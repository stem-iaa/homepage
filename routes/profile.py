from app import app
from app import db
from flask import Flask, render_template, request, redirect, url_for
import flask_login
from werkzeug.security import generate_password_hash, check_password_hash
import model
import json
import os
from api import Azure


def is_user(current_user, compare_to):
    is_user = False
    if not current_user.is_anonymous:
        if current_user.username == compare_to:
            is_user = True
    return is_user


@app.route("/profile/<username>", methods=["GET"])
def profile(username):
    profile_user = model.User.query.filter_by(username=username).first()

    if not profile_user:
        return "no user found"

    profiles = {
        "student": "student_profile.html",
        "mentor": "mentor_profile.html",
        "instructor": "instructor_profile.html"
    }

    current_user = flask_login.current_user

    return render_template(profiles.get(profile_user.discriminator),
                           user=current_user,
                           profile_user=profile_user,
                           is_user=is_user(current_user, username))


@app.route("/profile/<username>/info")
@flask_login.login_required
def info(username):
    profile_user = model.User.query.filter_by(username=username).first()
    if not profile_user:
        return "no user found"

    if profile_user.username != flask_login.current_user.username:
        return "no permission for user"

    all_instructors = model.Instructor.query.filter_by(discriminator="instructor").all()
    all_instructors = sorted(all_instructors, key=lambda x: x.label)

    return render_template("info.html",
                           user=flask_login.current_user,
                           profile_user=profile_user,
                           is_user=True,
                           instructors=all_instructors)


@app.route("/profile/<username>/account", methods=["GET"])
@flask_login.login_required
def account(username):
    profile_user = model.User.query.filter_by(username=username).first()
    if not profile_user:
        return "no user found"

    current_user = flask_login.current_user
    if profile_user.username != current_user.username and current_user.discriminator != "instructor":
        return "no permission for user"

    return render_template("account.html",
                           user=flask_login.current_user,
                           profile_user=profile_user,
                           is_user=is_user(current_user, username))


@app.route("/profile/<username>/update", methods=["POST"])
@flask_login.login_required
def update(username):
    profile_user = model.User.query.filter_by(username=username).first()
    if not profile_user:
        return json.dumps({
            "error": "No user found"
        })

    current_user = flask_login.current_user
    if profile_user.username != current_user.username and current_user.discriminator != "instructor":
        return json.dumps({
            "error": "No permission for user"
        })

    username_field = request.form.get("username")
    existing_user = model.User.query.filter_by(username=username_field).first()
    if existing_user and existing_user != profile_user:
        return json.dumps({
            "error": "Username already exists"
        })

    whitelisted_parameters = {
        "first_name", "last_name", "email", "location", "skype_id", "bio", "portfolio"
    }

    admin_parameters = {
        "label", "username", "vm_name", "worm_password"
    }

    for parameter in request.form.keys():
        if parameter in whitelisted_parameters.union(admin_parameters):
            value = request.form.get(parameter)
            if value:
                if parameter in admin_parameters and current_user.discriminator != "instructor":
                    return json.dumps({"error": "No permission to set " + parameter})
                setattr(profile_user, parameter, value)

    if profile_user.discriminator == "mentor":
        if request.form.get("students"):
            profile_user.students = []
            student_usernames = [username.strip() for username in request.form.get("students").split(",")]
            for student_username in student_usernames:
                student = model.Student.query.filter_by(username=student_username).first()
                if not student:
                    return json.dumps({"error": "Student not found: " + student_username})
                profile_user.students.append(student)

    db.session.commit()

    return json.dumps({
        "error": None,
        "info": {
            "username": profile_user.username
        }
    })


@app.route("/profile/<username>/picture", methods=["POST"])
@flask_login.login_required
def picture(username):
    profile_user = model.User.query.filter_by(username=username).first()
    if not profile_user:
        return json.dumps({
            "error": "No user found"
        })

    current_user = flask_login.current_user
    if profile_user.username != current_user.username:
        return json.dumps({
            "error": "No permission for user"
        })

    if "profile_picture" not in request.files:
        return json.dumps({
            "error": "No file"
        })

    profile_picture = request.files["profile_picture"]
    if not profile_picture.filename:
        return json.dumps({
            "error": "No file selected"
        })

    allowed_extensions = {"png", "jpg", "jpeg", "gif", "svg"}
    extension = profile_picture.filename.rsplit(".", 1)[1].lower()
    if extension not in allowed_extensions:
        return json.dumps({
            "error": "Picture invalid"
        })

    if profile_user.profile_picture_path:
        if os.path.isfile(profile_user.relative_profile_picture_path):
            os.remove(profile_user.relative_profile_picture_path)
    profile_picture_path = "static/images/profile_pictures/" + profile_user.username + "." + extension
    profile_picture.save(profile_picture_path)

    profile_user.profile_picture_path = "/" + profile_picture_path
    db.session.commit()

    return redirect("/profile/" + profile_user.username)


@app.route("/profile/<username>/password", methods=["POST"])
def password(username):
    profile_user = model.User.query.filter_by(username=username).first()
    if not profile_user:
        return json.dumps({
            "error": "No user found"
        })

    current_user = flask_login.current_user
    if profile_user.username != current_user.username:
        return json.dumps({
            "error": "No permission for user"
        })

    new_password = request.form.get("new_password")
    if not new_password:
        return json.dumps({"error": "New password required"})

    password_verify = request.form.get("verify_password")
    if not password_verify:
        return json.dumps({"error": "Password verification required"})

    if new_password != password_verify:
        return json.dumps({"error": "Password verification doesn't match password"})

    profile_user.password_hash = generate_password_hash(new_password)
    db.session.commit()

    return json.dumps({"error": None})


@app.route("/profile/<username>/worm_password", methods=["GET"])
@flask_login.login_required
def get_worm_password(username):
    profile_user = model.User.query.filter_by(username=username).first()
    if not profile_user:
        return json.dumps({
            "error": "No user found"
        })

    current_user = flask_login.current_user
    if current_user.discriminator == "student":
        return json.dumps({
            "error": "No permission for user"
        })

    if profile_user.worm_password:
        return json.dumps({
            "error": None,
            "worm_password": profile_user.worm_password
        })

    return json.dumps({
        "error": "User " + profile_user.username + " does not have a worm password"
    })


@app.route("/profile/<username>/content", methods=["GET", "POST"])
@flask_login.login_required
def content(username):
    profile_user = model.User.query.filter_by(username=username).first()
    if not profile_user:
        return json.dumps({
            "error": "No user found"
        })

    if request.method == "GET":
        return json.dumps(profile_user.portfolio)

    current_user = flask_login.current_user
    if current_user != profile_user:
        return json.dumps({"error": "No permission for user"})

    if not request.form.get("content"):
        return json.dumps({"error": "no content provided"})

    profile_user.portfolio = json.dumps(request.form.get("content"))
    db.session.commit()


@app.route("/admin")
@flask_login.login_required
def admin():
    current_user = flask_login.current_user
    if current_user.discriminator != "instructor":
        return json.dumps({
            "error": "No permission for user"
        })

    return render_template("admin.html",
                           user=current_user,
                           profile_user=current_user)
