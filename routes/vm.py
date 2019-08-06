from app import app
from app import db
from flask import Flask, render_template, request, redirect, url_for
import flask_login
from werkzeug.security import generate_password_hash, check_password_hash
import models
import json
from api import Azure


@app.route("/vm/status/<username>", methods=["GET"])
def status(username):
    return json.dumps(Azure.get_vm_status(username))


@app.route("/vm/start/<username>", methods=["POST"])
def start(username):
    current_user = flask_login.current_user
    if current_user.is_anonymous():
        return json.dumps({"error": "No permission for user"})

    Azure.start_vm(username)
    return json.dumps({"error": None})
