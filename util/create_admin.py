from app import db, model, generate_password_hash

admin = model.Instructor(username="sam", password_hash=generate_password_hash("sam"))

db.session.add(admin)
db.session.commit()
