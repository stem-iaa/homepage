from app import db


cohort_association_table = db.Table(
    "cohort_association", db.Model.metadata,
    db.Column("cohort", db.Integer, db.ForeignKey("cohort.id")),
    db.Column("user", db.Integer, db.ForeignKey("user.id"))
)


student_mentor_association_table = db.Table(
    "student_mentor_association", db.Model.metadata,
    db.Column("student", db.Integer, db.ForeignKey("student.id")),
    db.Column("mentor", db.Integer, db.ForeignKey("mentor.id"))
)
