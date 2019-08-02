from flask import Flask, render_template, request, redirect, url_for
import flask_login
import json
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.orm import joinedload


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
    return render_template("index.html")


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
def register():
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

    return render_template("info.html", user=flask_login.current_user, is_user=True)


@app.route("/profile/<username>/account", methods=["GET", "POST"])
@flask_login.login_required
def account(username):
    if request.method == "GET":
        profile_user = models.User.query.filter_by(username=username).first()
        if not profile_user:
            return "no user found"

        if profile_user.username != flask_login.current_user.username:
            return "no permission for user"

        return render_template("account.html", user=flask_login.current_user, is_user=True)
    elif request.method == "POST":
        pass


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

    whitelisted_parameters = {
        "first_name", "last_name", "email", "location", "bio", "portfolio"
    }

    for parameter in request.form.keys():
        if parameter in whitelisted_parameters:
            value = request.form.get(parameter)
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
        "error": None
    })


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
