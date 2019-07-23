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


class User(flask_login.UserMixin):
    pass


users = json.load(open("users.json", "r"))


@login_manager.user_loader
def user_loader(username):
    if username not in users:
        return None

    user = User()
    user.id = username
    return user


@app.route("/")
def hello_world():
    return render_template("index.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")
    elif request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        if not username or not password:
            return "Bad login"

        if password == users[username]["password"]:
            user = User()
            user.id = username
            flask_login.login_user(user)
            return redirect(url_for("protected"))

    return "Bad login"


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template("register.html")
    elif request.method == "POST":
        pass


@app.route("/protected")
@flask_login.login_required
def protected():
    return "protected"


@app.route("/test")
def test():
    return users


if __name__ == "__main__":
    app.run()
