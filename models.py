from app import db
from flask_login import UserMixin


class Student(UserMixin, db.Model):
    username = db.Column(db.String(64), index=True, unique=True, primary_key=True)
    password_hash = db.Column(db.String(128))
    name = db.Column(db.String(64), index=True)
    location = db.Column(db.String(128), index=True)
    email = db.Column(db.String(128), index=True, unique=True)
    bio = db.Column(db.String(1024))
    portfolio = db.Column(db.String(1024))
    mentor_username = db.Column(db.String(64), db.ForeignKey('mentor.username'))


class Mentor(UserMixin, db.Model):
    username = db.Column(db.String(64), index=True, unique=True, primary_key=True)
    password_hash = db.Column(db.String(128))
    name = db.Column(db.String(64), index=True)
    location = db.Column(db.String(128), index=True)
    email = db.Column(db.String(128), index=True, unique=True)
    bio = db.Column(db.String(1024))
    students = db.relationship("Student", backref="mentor", lazy="dynamic")
