from app import db
import os
import shutil


class SolutionFile(db.Model):
    __tablename__ = "solution_file"
    id = db.Column(db.Integer, index=True, primary_key=True)
    name = db.Column(db.String(128), index=True)

    solution_id = db.Column(db.Integer, db.ForeignKey("solution.id"))
    solution = db.relationship("Solution", back_populates="files")

    def __init__(self, **kwargs):
        super(SolutionFile, self).__init__(**kwargs)

        file = kwargs.get("file")
        if file:
            self.create_file(file)

    def create_file(self, file):
        file.save(self.relative_file_path)

    def delete_file(self):
        if os.path.exists(self.relative_file_path):
            os.remove(self.relative_file_path)

    @property
    def file_path(self):
        return self.solution.solutions_dir + "/" + str(self.id)

    @property
    def relative_file_path(self):
        return self.file_path[1:]

    @property
    def content(self):
        try:
            return open(self.relative_file_path, "r").read()
        except UnicodeDecodeError:
            return "Unable to display content."


class Solution(db.Model):
    __tablename__ = "solution"
    id = db.Column(db.Integer, index=True, primary_key=True)
    name = db.Column(db.String(128), index=True)

    cohort_id = db.Column(db.Integer, db.ForeignKey("cohort.id"))
    cohort = db.relationship("Cohort", back_populates="solutions")

    files = db.relationship("SolutionFile", back_populates="solution")

    def create_dir(self):
        cohort_solutions_dir = "/".join(self.relative_solutions_dir.split("/")[:-1])
        if not os.path.isdir(cohort_solutions_dir):
            os.mkdir(cohort_solutions_dir)
        if not os.path.isdir(self.relative_solutions_dir):
            os.mkdir(self.relative_solutions_dir)

    def delete_dir(self):
        if os.path.isdir(self.relative_solutions_dir):
            shutil.rmtree(self.relative_solutions_dir)

    @property
    def solutions_dir(self):
        return "/static/protected/solutions/" + str(self.cohort_id) + "/" + str(self.id)

    @property
    def relative_solutions_dir(self):
        return self.solutions_dir[1:]
