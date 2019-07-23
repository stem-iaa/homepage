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
def user_loader(username):
    student = models.Student.query.get(username)
    if student:
        return student

    mentor = models.Mentor.query.get(username)
    return mentor


@app.route("/")
def hello_world():
    return render_template("index.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if flask_login.current_user.is_authenticated:
        return redirect("/student/" + flask_login.current_user.username)

    if request.method == "GET":
        return render_template("login.html")
    elif request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        if not username or not password:
            return "Bad login"

        student = models.Student.query.filter(username=username).first()
        mentor = models.Mentor.query.filter(username=username).first()
        user = student or mentor

        if user is None or not check_password_hash(user.password_hash, password):
            return redirect(url_for("login"))

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
