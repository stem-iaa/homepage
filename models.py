from app import db
from flask_login import UserMixin


class User(UserMixin, db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    first_name = db.Column(db.String(64), index=True)
    last_name = db.Column(db.String(64), index=True)
    location = db.Column(db.String(128), index=True)
    email = db.Column(db.String(128), index=True, unique=True)
    bio = db.Column(db.String(1024))
    label = db.Column(db.String(128), index=True)

    discriminator = db.Column(db.String(50))

    type = "User"

    mapper_args__ = {
        "polymorphic_identity": "user",
        "polymorphic_on": discriminator
    }

    def __init__(self, **kwargs):
        super(User, self).__init__(**kwargs)

        if not self.label:
            self.label = self.type


student_mentor_association_table = db.Table(
    "student_mentor_association", db.Model.metadata,
    db.Column("student", db.Integer, db.ForeignKey("student.id")),
    db.Column("mentor", db.Integer, db.ForeignKey("mentor.id"))
)


class Student(User):
    __tablename__ = "student"
    id = db.Column(db.Integer, db.ForeignKey("user.id"), primary_key=True)
    portfolio = db.Column(db.String(1024))

    type = "Student"

    mentors = db.relationship(
        "Mentor",
        secondary=student_mentor_association_table,
        back_populates="students"
    )

    mapper_args__ = {
        "polymorphic_identity": "student"
    }

    def __init__(self, **kwargs):
        super(Student, self).__init__(**kwargs)


class Mentor(User):
    __tablename__ = "mentor"
    id = db.Column(db.Integer, db.ForeignKey("user.id"), primary_key=True)

    type = "Mentor"

    students = db.relationship(
        "Student",
        secondary=student_mentor_association_table,
        back_populates="mentors"
    )

    mapper_args__ = {
        "polymorphic_identity": "mentor"
    }

    def __init__(self, **kwargs):
        super(Mentor, self).__init__(**kwargs)


class Instructor(User):
    __tablename__ = "instructor"
    id = db.Column(db.Integer, db.ForeignKey("user.id"), primary_key=True)

    type = "Instructor"

    mapper_args__ = {
        "polymorphic_identity": "instructor"
    }

    def __init__(self, **kwargs):
        super(Instructor, self).__init__(**kwargs)
