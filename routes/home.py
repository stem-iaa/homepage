from app import app
from flask import Flask, render_template, request, redirect, url_for
import flask_login
import model


@app.route("/")
def home():
    current_user = flask_login.current_user
    if current_user.is_anonymous:
        return render_template("index.html", user=flask_login.current_user)
    else:
        return redirect("/profile/" + current_user.username)
