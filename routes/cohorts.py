from app import app
from app import db
from flask import Flask, render_template, request, redirect, url_for
import flask_login
from werkzeug.security import generate_password_hash, check_password_hash
import models
import json


@app.route("/cohorts", methods=["GET"])
@flask_login.login_required
def cohorts():
    current_user = flask_login.current_user
    if current_user.discriminator != "instructor":
        return "no permission for user"

    return render_template("cohorts.html",
                           user=current_user,
                           cohorts=models.Cohort.query.all())


@app.route("/cohort", methods=["GET", "POST"])
@flask_login.login_required
def cohort():
    current_user = flask_login.current_user
    if request.method == "GET":
        return render_template("cohort.html",
                               user=current_user)

    if current_user.discriminator != "instructor":
        return "no permission for user"

    name = request.form.get("name")
    is_active = request.form.get("is_active")

    # create new
    if not name:
        return json.dumps({"error": "no name given"})

    existing_cohort = models.Cohort.query.filter_by(id=name).first()
    if existing_cohort:
        return json.dumps({"error": "cohort already exists with name: " + name})

    new_cohort = models.Cohort(name=name, active=True if is_active else False)
    db.session.add(new_cohort)

    db.session.commit()

    return json.dumps({"error": None})


@app.route("/cohort/<id>", methods=["GET", "POST", "DELETE"])
def specific_cohort(id):
    cohort = models.Cohort.query.filter_by(id=id).first()
    if not cohort:
        return json.dumps({"error": "no cohort found for id " + id})

    current_user = flask_login.current_user
    if request.method == "GET":
        return render_template("cohort.html",
                               user=current_user,
                               cohort=cohort)

    if current_user.discriminator != "instructor":
        return "no permission for user"

    if request.method == "DELETE":
        db.session.delete(cohort)
        return json.dumps({"error": None})

    # update existing
    name = request.form.get("name")
    is_active = request.form.get("is_active")

    if name is not None and name != cohort.name:
        existing_cohort = models.Cohort.query.filter_by(name=name).first()
        if existing_cohort:
            return json.dumps({"error": "cohort already exists with name: " + name})
        cohort.name = name

    if is_active is not None:
        cohort.active = is_active

    db.session.commit()

    return json.dumps({
        "error": None,
        "name": cohort.name,
        "is_active": cohort.active
    })

