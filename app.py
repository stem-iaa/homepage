from flask import Flask, render_template, request, redirect, url_for, abort
import flask_login
import json
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
import os
from flask_migrate import Migrate


config = json.load(open("config.json", "r"))


# https://stackoverflow.com/questions/12118355/secure-static-files-with-flask
class SecuredStaticFlask(Flask):
    def send_static_file(self, filename):
        root_dir = filename.split("/")[0]
        if root_dir != "protected":
            return super(SecuredStaticFlask, self).send_static_file(filename)

        current_user = flask_login.current_user
        if current_user.is_anonymous:
            abort(403)
        if current_user.discriminator == "student":
            abort(403)

        return super(SecuredStaticFlask, self).send_static_file(filename)


app = SecuredStaticFlask(__name__)
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


import routes


if __name__ == "__main__":
    app.run()
