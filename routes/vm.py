from app import app
from app import db
from flask import Flask, render_template, request, redirect, url_for
import flask_login
from werkzeug.security import generate_password_hash, check_password_hash
import model
import json
from api import Azure
import msrestazure.azure_exceptions
from .profile import is_user


@app.route("/vm/status/<username>", methods=["GET"])
def status(username):
    user = model.User.query.filter_by(username=username).first()
    if not user:
        return json.dumps({"error": "no user found for username: " + username})

    try:
        status = Azure.get_vm_status(user.vm_name)
    except msrestazure.azure_exceptions.CloudError as cloud_error:
        return json.dumps({"error": cloud_error.message})

    return json.dumps({
        "error": None,
        "status": status
    })


@app.route("/vm/start/<username>", methods=["POST"])
@flask_login.login_required
def start(username):
    user = model.User.query.filter_by(username=username).first()
    if not user:
        return json.dumps({"error": "no user found for username: " + username})

    if flask_login.current_user.discriminator == "student":
        if not is_user(flask_login.current_user, username):
            return json.dumps({"error": "Permission denied for user."})

    try:
        Azure.start_vm(user.vm_name)
    except msrestazure.azure_exceptions.CloudError as cloud_error:
        return json.dumps({"error": cloud_error.message})

    return json.dumps({"error": None})


@app.route("/vm/ip/<username>", methods=["GET"])
def ip(username):
    user = model.User.query.filter_by(username=username).first()

    current_user = flask_login.current_user
    if user != current_user and current_user.discriminator == "student":
        return json.dumps({"error": "no permission for user"})

    if not user:
        return json.dumps({"error": "no user found for username: " + username})
    try:
        ip = Azure.get_vm_ip(user.vm_name)
    except msrestazure.azure_exceptions.CloudError as cloud_error:
        return json.dumps({"error": cloud_error.message})

    return json.dumps({
        "error": None,
        "ip": ip,
        "password": user.worm_password
    })
