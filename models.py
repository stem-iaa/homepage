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
    email = db.Column(db.String(128), index=True)
    bio = db.Column(db.String(1024))
    label = db.Column(db.String(128), index=True)
    portfolio = db.Column(db.String(1024))
    profile_picture_path = db.Column(db.String(128))
    skype_id = db.Column(db.String(128))

    discriminator = db.Column(db.String(50), index=True)

    __mapper_args__ = {
        "polymorphic_identity": "user",
        "polymorphic_on": discriminator
    }

    def __init__(self, **kwargs):
        super(User, self).__init__(**kwargs)

        if not self.label:
            self.label = self.discriminator.capitalize()

    @property
    def full_name(self):
        if not self.first_name or not self.last_name:
            return None
        return self.first_name + " " + self.last_name

    @property
    def stylized_username(self):
        return "@" + self.username

    @property
    def profile_picture_path_or_default(self):
        return self.profile_picture_path if self.profile_picture_path else "/static/images/default_profile.svg"

    @property
    def relative_profile_picture_path(self):
        if not self.profile_picture_path:
            return None
        return self.profile_picture_path[1:]


student_mentor_association_table = db.Table(
    "student_mentor_association", db.Model.metadata,
    db.Column("student", db.Integer, db.ForeignKey("student.id")),
    db.Column("mentor", db.Integer, db.ForeignKey("mentor.id"))
)


class Student(User):
    __tablename__ = "student"
    id = db.Column(db.Integer, db.ForeignKey("user.id"), primary_key=True)

    mentors = db.relationship(
        "Mentor",
        secondary=student_mentor_association_table,
        back_populates="students",
        lazy="joined"
    )

    __mapper_args__ = {
        "polymorphic_identity": "student"
    }

    @property
    def mentor_usernames_list(self):
        names = [mentor.username for mentor in self.mentors]
        return ", ".join(names)


class Mentor(User):
    __tablename__ = "mentor"
    id = db.Column(db.Integer, db.ForeignKey("user.id"), primary_key=True)

    students = db.relationship(
        "Student",
        secondary=student_mentor_association_table,
        back_populates="mentors",
        lazy="joined"
    )

    __mapper_args__ = {
        "polymorphic_identity": "mentor"
    }

    @property
    def student_usernames_list(self):
        names = [student.username for student in self.students]
        return ", ".join(names)


class Instructor(User):
    __tablename__ = "instructor"
    id = db.Column(db.Integer, db.ForeignKey("user.id"), primary_key=True)

    __mapper_args__ = {
        "polymorphic_identity": "instructor"
    }
