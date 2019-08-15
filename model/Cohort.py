from app import db
from .User import Instructor
from .Maps import cohort_association_table


class Cohort(db.Model):
    __tablename__ = "cohort"
    id = db.Column(db.Integer, index=True, primary_key=True)
    name = db.Column(db.String, index=True, unique=True)
    active = db.Column(db.Boolean, index=True)

    users = db.relationship(
        "User",
        secondary=cohort_association_table,
        back_populates="cohorts",
        lazy="joined"
    )

    def __init__(self, **kwargs):
        super(Cohort, self).__init__(**kwargs)

        all_instructors = Instructor.query.all()
        for instructor in all_instructors:
            self.users.append(instructor)
