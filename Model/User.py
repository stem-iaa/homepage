from app import db


class User(db.Model):
    username = db.Column(db.String(64), index=True, unique=True, primary_key=True)
    password_hash = db.Column(db.String(128))
    user_type = db.Column(db.String(64))

