from app import app
from app import db
from flask import Flask, render_template, request, redirect, url_for, abort
import flask_login
from werkzeug.security import generate_password_hash, check_password_hash
import model
import json
from sqlalchemy import or_


@app.route("/solutions", methods=["GET"])
@flask_login.login_required
def solutions():
    current_user = flask_login.current_user
    if current_user.discriminator == "student":
        abort(403)

    return render_template("solutions.html",
                           user=current_user,
                           cohorts=model.Cohort.query.all())

