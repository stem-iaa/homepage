from app import app
from app import db
from flask import Flask, render_template, request, redirect, url_for
import flask_login
from werkzeug.security import generate_password_hash, check_password_hash
import models
import json


@app.route("/login", methods=["GET", "POST"])
def login():
    if flask_login.current_user.is_authenticated:
        return redirect("/profile/" + flask_login.current_user.username)

    if request.method == "GET":
        return render_template("login.html")
    elif request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        if not username or not password:
            return "Bad login"

        user = models.User.query.filter_by(username=username).first()

        if user is None or not check_password_hash(user.password_hash, password):
            return "Bad login"

        flask_login.login_user(user)
        return redirect("/profile/" + user.username)

    return "Bad login"


@app.route("/register", methods=["GET", "POST"])
@flask_login.login_required
def register():
    current_user = flask_login.current_user
    if current_user.discriminator != "instructor":
        return json.dumps({
            "error": "No permission for user"
        })

    if request.method == "GET":
        return render_template("register.html",
                               user=current_user)

    username = request.form.get("username")
    if not username:
        return json.dumps({
            "error": "Username required"
        })

    existing_user = models.User.query.filter_by(username=username).first()
    if existing_user:
        return json.dumps({
            "error": "Username already exists"
        })

    password = request.form.get("password")
    if not password:
        return json.dumps({
            "error": "Password required"
        })

    info = {
        "username": username,
        "password_hash": generate_password_hash(request.form.get("password")),
        "first_name": request.form.get("first_name"),
        "last_name": request.form.get("last_name"),
        "email": request.form.get("email"),
        "location": request.form.get("location"),
        "skype_id": request.form.get("skype_id")
    }

    for key in info:
        if not info[key]:
            info[key] = None

    if info["email"]:
        existing_user = models.User.query.filter_by(email=info["email"]).first()
        if existing_user:
            return json.dumps({
                "error": "Email already used"
            })

    user_type = request.form.get("user_type")

    user = None
    if user_type == "student":
        mentor_list = request.form.get("mentors").strip()
        if mentor_list:
            info["mentors"] = []
            mentor_usernames = [username.strip() for username in mentor_list.split(",")]
            print(mentor_usernames)
            for mentor_username in mentor_usernames:
                mentor = models.Mentor.query.filter_by(username=mentor_username).first()
                if not mentor:
                    return json.dumps({
                        "error": "Mentor not found: " + mentor_username
                    })
                info["mentors"].append(mentor)
        user = models.Student(**info)
    elif user_type == "mentor":
        student_list = request.form.get("students").strip()
        if student_list:
            info["students"] = []
            student_usernames = [username.strip() for username in request.form.get("students").split(",")]
            for student_username in student_usernames:
                student = models.Student.query.filter_by(username=student_username).first()
                if not student:
                    return json.dumps({
                        "error": "Student not found: " + student_username
                    })
                info["students"].append(student)
        user = models.Mentor(**info)
    else:
        user = models.Instructor(**info)

    db.session.add(user)
    db.session.commit()

    return json.dumps({
        "error": None,
        "info": {
            "username": username
        }
    })


@app.route("/current_user", methods=["GET"])
def current_user():
    current_user = flask_login.current_user
    return json.dumps({
        "current_user": None if current_user.is_anonymous else current_user.username
    })


@app.route("/logout")
def logout():
    flask_login.logout_user()
    return redirect("/")
