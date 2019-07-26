from flask import Flask, render_template, request, redirect, url_for
import flask_login
import json
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from werkzeug.security import generate_password_hash, check_password_hash

config = json.load(open("config.json", "r"))

app = Flask(__name__)
app.secret_key = config["secret"]
app.config["SQLALCHEMY_DATABASE_URI"] = config["SQLALCHEMY_DATABASE_URI"]
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)
migrate = Migrate(app, db)

login_manager = flask_login.LoginManager()
login_manager.init_app(app)

import models


def get_user(username):
    student = models.Student.query.filter_by(username=username).first()
    mentor = models.Mentor.query.filter_by(username=username).first()
    user = student or mentor

    return user


@login_manager.user_loader
def user_loader(id):
    student = models.Student.query.get(id)
    if student:
        return student

    mentor = models.Mentor.query.get(id)
    return mentor


@app.route("/")
def hello_world():
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

        user = get_user(username)

        if user is None or not check_password_hash(user.password_hash, password):
            return "Bad login"

        flask_login.login_user(user)
        return redirect("/profile/" + user.username)

    return "Bad login"


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template("register.html")
    elif request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        user_type = request.form.get("user_type")

        if not username or not password or not user_type:
            return "Bad register"

        user = None
        if user_type == "student":
            user = models.Student(username=username, password_hash=generate_password_hash(password))
        elif user_type == "mentor":
            user = models.Mentor(username=username, password_hash=generate_password_hash(password))

        if not user:
            return "Bad register"

        db.session.add(user)
        db.session.commit()

        flask_login.login_user(user)
        return redirect("/profile/" + user.username)


@app.route("/profile/<username>", methods=["GET"])
def profile(username):
    current_user = flask_login.current_user
    is_user = False
    if not current_user.is_anonymous:
        if current_user.username == username:
            is_user = True

    user = get_user(username)

    if user:
        return render_template("profile.html",
                               user=get_user(username),
                               profile_user=user,
                               is_user=is_user)
    else:
        return "no user found"


@app.route("/protected")
@flask_login.login_required
def protected():
    return "protected"


@app.route("/test")
def test():
    return render_template("profile.html", user=models.Student.query.all()[0])


if __name__ == "__main__":
    app.run()
