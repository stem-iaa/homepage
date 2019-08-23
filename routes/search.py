from app import app
from app import db
from flask import Flask, render_template, request, redirect, url_for
import flask_login
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy import or_
import model
import json


def query_users(query_string, limit=None, restrict_to_cohort=None):
    query = model.User.query.filter(or_(
        model.User.username.contains(query_string),
        model.User.first_name.contains(query_string),
        model.User.last_name.contains(query_string),
        model.User.label.contains(query_string),
        model.User.email.contains(query_string)
    ))

    if limit:
        query = query.limit(limit).all()
    else:
        query = query.all()


@app.route("/api/search/", methods=["GET"])
@app.route("/api/search/<query_string>", methods=["GET"])
@app.route("/api/search/<query_string>/<limit>")
@flask_login.login_required
def search_api(query_string="", limit=None):
    if not query_string:
        return json.dumps([])

    query = model.User.query.filter(or_(
        model.User.username.contains(query_string),
        model.User.first_name.contains(query_string),
        model.User.last_name.contains(query_string),
        model.User.label.contains(query_string),
        model.User.email.contains(query_string)
    ))

    if limit:
        try:
            limit = int(limit)
        except ValueError:
            limit = None

    if limit:
        query = query.limit(limit).all()
    else:
        query = query.all()

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
