from app import db


class SolutionFile(db.Model):
    __tablename__ = "solution_file"
    id = db.Column(db.Integer, index=True, primary_key=True)
    name = db.Column(db.String(128), index=True)
    path = db.Column(db.String(256))

    solution_id = db.Column(db.Integer, db.ForeignKey("solution.id"))
    solution = db.relationship("Solution", back_populates="files")


class Solution(db.Model):
    __tablename__ = "solution"
    id = db.Column(db.Integer, index=True, primary_key=True)
    name = db.Column(db.String(128), index=True)

    cohort_id = db.Column(db.Integer, db.ForeignKey("cohort.id"))
    cohort = db.relationship("Cohort", back_populates="solutions")

    files = db.relationship("SolutionFile", back_populates="solution")
