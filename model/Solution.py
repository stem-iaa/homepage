from app import db


class File(db.Model):
    __tablename__ = "file"

    id = db.Column(db.Integer, index=True, primary_key=True)
    path = db.Column(db.String(128), index=True)
    solution = db.relationship("Solution", db.ForeignKey("solution.id"))


class Solution(db.Model):
    __tablename__ = "solution"

    id = db.Column(db.Integer, index=True, primary_key=True)
    name = db.Column(db.String(128), index=True)
    notes = db.Column(db.String(1024))
    files = db.relationship("File")
    cohort = db.relationship("Cohort", db.ForeignKey("cohort.id"))
