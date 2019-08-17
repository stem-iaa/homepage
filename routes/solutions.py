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
        return abort(403)

    return render_template("solutions.html",
                           user=current_user)


@app.route("/solutions/<cohort_id>", methods=["GET"])
@flask_login.login_required
def solutions_for_cohort(cohort_id):
    current_user = flask_login.current_user
    if current_user.discriminator == "student":
        return abort(403)

    cohort = model.Cohort.query.filter_by(id=cohort_id).first()
    if not cohort:
        return json.dumps({"error": "no cohort found for id: " + cohort_id})

    return render_template("solutions_for_cohort.html",
                           user=current_user,
                           cohort=cohort)


@app.route("/solution", methods=["POST"])
@flask_login.login_required
def add_solution():
    current_user = flask_login.current_user
    if current_user.discriminator != "instructor":
        return abort(403)

    cohort_id = request.form.get("cohort_id")
    if not cohort_id:
        return json.dumps({"error": "cohort id required"})

    cohort = model.Cohort.query.filter_by(id=cohort_id).first()
    if not cohort:
        return json.dumps({"error": "cohort not found for id: " + cohort_id})

    name = request.form.get("name")

    new_solution = model.Solution(name=name, cohort=cohort)
    db.session.add(new_solution)
    db.session.commit()

    return json.dumps({"error": None})


@app.route("/solution/<id>", methods=["GET", "POST", "DELETE"])
@flask_login.login_required
def solution(id):
    current_user = flask_login.current_user
    if current_user.discriminator == "student":
        abort(403)

    if request.method == "GET":
        return "solution for " + id

    if current_user.discriminator != "instructor":
        return json.dumps({"error": "no permission for user"})

    solution = model.Solution.query.filter_by(id=id).first()
    if not solution:
        return json.dumps({"error": "no solution found for id: " + id})

    if request.method == "DELETE":
        db.session.delete(solution)
        db.session.commit()
        return json.dumps({"error": None})

    name = request.form.get("name")
    if name:
        solution.name = name

    for file_obj in request.files:
        print(file_obj)

    db.session.commit()

    return json.dumps({
        "error": None,
        "name": solution.name
    })
