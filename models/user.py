from flask_login import UserMixin
from models import db

class User(UserMixin, db.Model):  # ✅ Inherit from UserMixin
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)



class UserFormData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False, unique=True)
    data = db.Column(db.PickleType)

    user = db.relationship('User', backref=db.backref('form_data', uselist=False))