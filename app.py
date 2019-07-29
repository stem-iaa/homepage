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


@login_manager.user_loader
def user_loader(id):
    user = models.User.query.get(id)
    if user:
        return user
    return None


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
    profile_user = models.User.query.filter_by(username=username).first()
    if not profile_user:
        return "no user found"

    current_user = flask_login.current_user
    is_user = False
    if not current_user.is_anonymous:
        if current_user.username == username:
            is_user = True

    return render_template("profile.html",
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

    current_user = flask_login.current_user
    is_user = False
    if not current_user.is_anonymous:
        if current_user.username == username:
            is_user = True

    return render_template("info.html",
                           user=current_user,
                           is_user=is_user)


@app.route("/profile/<username>/account")
@flask_login.login_required
def account(username):
    return "protected"


@app.route("/test")
def test():
    return render_template("profile.html", user=models.Student.query.all()[0])


if __name__ == "__main__":
    app.run()
