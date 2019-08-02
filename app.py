from flask import Flask, render_template, request, redirect, url_for
import flask_login
import json
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy import or_
import os


config = json.load(open("config.json", "r"))

app = Flask(__name__)
app.secret_key = config["secret"]
app.config["SQLALCHEMY_DATABASE_URI"] = config["SQLALCHEMY_DATABASE_URI"]
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

login_manager = flask_login.LoginManager()
login_manager.init_app(app)

import models


@login_manager.user_loader
def user_loader(id):
    user = models.User.query.get(id)
    if user:
        return user
    return None


@app.route("/")
def home():
    return render_template("index.html", user=flask_login.current_user)


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
        return render_template("register.html")

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
        "location": request.form.get("location")
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


@app.route("/profile/<username>", methods=["GET"])
def profile(username):
    profile_user = models.User.query.filter_by(username=username).first()

    if not profile_user:
        return "no user found"

    current_user = flask_login.current_user
    is_user = False
    if not current_user.is_anonymous:
        if current_user.username == username:
            is_user = True

    profiles = {
        "student": "student_profile.html",
        "mentor": "mentor_profile.html",
        "instructor": "instructor_profile.html"
    }

    return render_template(profiles.get(profile_user.discriminator),
                           user=current_user,
                           profile_user=profile_user,
                           is_user=is_user)


@app.route("/profile/<username>/info")
@flask_login.login_required
def info(username):
    profile_user = models.User.query.filter_by(username=username).first()
    if not profile_user:
        return "no user found"

    if profile_user.username != flask_login.current_user.username:
        return "no permission for user"

    all_instructors = models.Instructor.query.filter_by(discriminator="instructor").all()

    return render_template("info.html",
                           user=flask_login.current_user,
                           profile_user=profile_user,
                           is_user=True,
                           instructors=all_instructors)


@app.route("/profile/<username>/account", methods=["GET"])
@flask_login.login_required
def account(username):
    profile_user = models.User.query.filter_by(username=username).first()
    if not profile_user:
        return "no user found"

    if profile_user.username != flask_login.current_user.username:
        return "no permission for user"

    return render_template("account.html",
                           user=flask_login.current_user,
                           profile_user=profile_user,
                           is_user=True)


@app.route("/profile/<username>/update", methods=["POST"])
@flask_login.login_required
def update(username):
    profile_user = models.User.query.filter_by(username=username).first()
    if not profile_user:
        return json.dumps({
            "error": "No user found"
        })

    current_user = flask_login.current_user
    if profile_user.username != current_user.username:
        return json.dumps({
            "error": "No permission for user"
        })

    existing_user = models.User.query.filter_by(username=username).first()
    if existing_user and existing_user != profile_user:
        return json.dumps({
            "error": "Username already exists"
        })

    if request.form.get("email"):
        existing_user = models.User.query.filter_by(email=request.form.get("email")).first()
        if existing_user and existing_user != profile_user:
            return json.dumps({
                "error": "Email already used"
            })

    whitelisted_parameters = {
        "username", "first_name", "last_name", "email", "location", "bio", "portfolio"
    }

    for parameter in request.form.keys():
        if parameter in whitelisted_parameters:
            value = request.form.get(parameter)
            if value:
                setattr(profile_user, parameter, value)

    if profile_user.discriminator == "mentor":
        if request.form.get("students"):
            profile_user.students = []
            student_usernames = [username.strip() for username in request.form.get("students").split(",")]
            for student_username in student_usernames:
                student = models.Student.query.filter_by(username=student_username).first()
                if not student:
                    return json.dumps({
                        "error": "Student not found: " + student_username
                    })
                profile_user.students.append(student)

    if profile_user.discriminator == "instructor":
        if request.form.get("label"):
            profile_user.label = request.form.get("label")

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
    profile_user = models.User.query.filter_by(username=username).first()
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
    profile_user = models.User.query.filter_by(username=username).first()
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


@app.route("/search/", methods=["GET"])
@app.route("/search/<query_string>", methods=["GET"])
def search(query_string=""):
    if not query_string:
        return json.dumps([])

    query = models.User.query.filter(or_(
        models.User.username.contains(query_string),
        models.User.first_name.contains(query_string),
        models.User.last_name.contains(query_string),
        models.User.label.contains(query_string),
        models.User.email.contains(query_string)
    )).all()

    ret = []
    for result in query:
        ret.append({
            "username": result.username,
            "stylized_username": result.stylized_username,
            "full_name": result.full_name
        })
    return json.dumps(ret)


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


@app.route("/logout")
def logout():
    flask_login.logout_user()
    return redirect("/")


@app.route("/current_user", methods=["GET"])
def current_user():
    current_user = flask_login.current_user
    return json.dumps({
        "current_user": None if current_user.is_anonymous else current_user.username
    })


@app.route("/test")
def test():
    return render_template("profile.html", user=models.Student.query.all()[0])


if __name__ == "__main__":
    app.run()
