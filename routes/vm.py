from app import app
from app import db
from flask import Flask, render_template, request, redirect, url_for
import flask_login
from werkzeug.security import generate_password_hash, check_password_hash
import models
import json
from api import Azure
import msrestazure.azure_exceptions
from .profile import is_user


@app.route("/vm/status/<username>", methods=["GET"])
def status(username):
    try:
        status = Azure.get_vm_status(username)
    except msrestazure.azure_exceptions.CloudError as cloud_error:
        return json.dumps({"error": cloud_error.message})

    return json.dumps({
        "error": None,
        "status": status
    })


@app.route("/vm/start/<username>", methods=["POST"])
@flask_login.login_required
def start(username):
    if not is_user(flask_login.current_user, username):
        return json.dumps({"error": "Permission denied for user."})

    try:
        Azure.start_vm(username)
    except msrestazure.azure_exceptions.CloudError as cloud_error:
        return json.dumps({"error": cloud_error.message})

    return json.dumps({"error": None})
