from app import db
from flask_login import UserMixin
from sqlalchemy.ext.hybrid import hybrid_property
from .Maps import cohort_association_table, student_mentor_association_table


class User(UserMixin, db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    first_name = db.Column(db.String(64), index=True)
    last_name = db.Column(db.String(64), index=True)
    location = db.Column(db.String(128), index=True)
    email = db.Column(db.String(128))
    bio = db.Column(db.String(1024))
    label = db.Column(db.String(128), index=True)
    portfolio = db.Column(db.String(1024))
    profile_picture_path = db.Column(db.String(128))
    skype_id = db.Column(db.String(128))
    _vm_name = db.Column(db.String(64), index=True)
    worm_password = db.Column(db.String(20))  # vm password

    cohorts = db.relationship(
        "Cohort",
        secondary=cohort_association_table,
        back_populates="users",
        lazy="joined"
    )

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

    @hybrid_property
    def vm_name(self):
        if self._vm_name:
            return self._vm_name
        return self.username

    @vm_name.setter
    def vm_name(self, value):
        self._vm_name = value


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
