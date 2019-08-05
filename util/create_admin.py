from ..app import db, models, generate_password_hash

admin = models.Instructor(username="sam", password_hash=generate_password_hash("sam"))

db.session.add(admin)
db.session.commit()
