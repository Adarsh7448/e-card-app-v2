from .database import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.Text, unique = True, nullable = False)
    email = db.Column(db.Text, unique = True, nullable = False)
    password = db.Column(db.Text, nullable = False)
    role = db.Column(db.Text, nullable = False, default = "user")

class UserCardDetail(db.Model):
    id = db.Column(db.Integer, primary_key = True)

