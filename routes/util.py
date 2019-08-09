from app import app
from app import db
from flask import Flask, render_template, request, redirect, url_for
import flask_login
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy import or_
import models
import json


@app.route("/search/", methods=["GET"])
@app.route("/search/<query_string>", methods=["GET"])
@flask_login.login_required
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

    current_user = flask_login.current_user

    # TODO more efficient query join
    cohort_users = []
    for cohort in current_user.cohorts:
        for user in cohort.users:
            cohort_users.append(user)

    cohort_users = [user for user in query if user in cohort_users]

    ret = []
    for result in cohort_users:
        ret.append({
            "username": result.username,
            "stylized_username": result.stylized_username,
            "full_name": result.full_name,
            "label": result.label
        })
    return json.dumps(ret)
