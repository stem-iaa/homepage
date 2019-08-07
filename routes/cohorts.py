from app import app
from app import db
from flask import Flask, render_template, request, redirect, url_for
import flask_login
from werkzeug.security import generate_password_hash, check_password_hash
import models
import json


@app.route("/cohorts", methods=["GET"])
def cohorts():
    current_user = flask_login.current_user
    if current_user.discriminator != "instructor":
        return "no permission for user"

    return render_template("cohorts.html",
                           user=current_user)
