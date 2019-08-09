from app import app
from app import db
from flask import Flask, render_template, request, redirect, url_for
import flask_login
from werkzeug.security import generate_password_hash, check_password_hash
import models
import json
from sqlalchemy import or_


@app.route("/cohorts", methods=["GET"])
@flask_login.login_required
def cohorts():
    current_user = flask_login.current_user
    if current_user.discriminator != "instructor":
        return "no permission for user"

    return render_template("cohorts.html",
                           user=current_user,
                           cohorts=models.Cohort.query.all())


@app.route("/cohort", methods=["POST"])
@flask_login.login_required
def cohort():
    current_user = flask_login.current_user
    if current_user.discriminator != "instructor":
        return json.dumps({"error": "no permission for user"})

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
    if current_user not in cohort.users:
        return json.dumps({"error": "no permission for user"})

    if request.method == "GET":
        instructors = []
        mentors = []
        students = []
        for user in cohort.users:
            if user.discriminator == "instructor":
                instructors.append(user)
            elif user.discriminator == "mentor":
                mentors.append(user)
            elif user.discriminator == "student":
                students.append(user)

        instructors = sorted(instructors, key=lambda x: x.label)

        return render_template("cohort.html",
                               user=current_user,
                               cohort=cohort,
                               instructors=instructors,
                               mentors=mentors,
                               students=students)

    if current_user.discriminator != "instructor":
        return json.dumps({"error": "no permission for user"})

    if request.method == "DELETE":
        db.session.delete(cohort)
        db.session.commit()
        return json.dumps({"error": None})

    # update existing
    name = request.form.get("name")
    is_active = request.form.get("is_active")
    if is_active:
        is_active = True if request.form.get("is_active") == "true" else False

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


@app.route("/cohort/<id>/add_user/<username>", methods=["POST"])
def add_user(id, username):
    cohort = models.Cohort.query.filter_by(id=id).first()
    if not cohort:
        return json.dumps({"error": "no cohort found for id " + id})

    user = models.User.query.filter_by(username=username).first()
    if not user:
        return json.dumps({"error": "no user found for username " + username})

    if cohort not in user.cohorts:
        user.cohorts.append(cohort)

    db.session.commit()

    return json.dumps({
        "error": None
    })


@app.route("/cohort/<id>/add_user_search/", methods=["GET"])
@app.route("/cohort/<id>/add_user_search/<query_string>", methods=["GET"])
def add_user_search(id, query_string=""):
    if not query_string:
        return json.dumps([])

    cohort = models.Cohort.query.filter_by(id=id).first()
    if not cohort:
        return json.dumps({"error": "no cohort found for id " + id})

    query = models.User.query.filter(or_(
        models.User.username.contains(query_string),
        models.User.first_name.contains(query_string),
        models.User.last_name.contains(query_string),
        models.User.label.contains(query_string),
        models.User.email.contains(query_string)
    )).all()

    new_users = [user for user in query if user not in cohort.users]

    ret = []
    for result in new_users:
        ret.append({
            "username": result.username,
            "stylized_username": result.stylized_username,
            "full_name": result.full_name,
            "label": result.label
        })
    return json.dumps(ret)
