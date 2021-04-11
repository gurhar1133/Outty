# models.py
from flask_login import UserMixin
from . import db


class User(UserMixin, db.Model):
    # primary keys are required by SQLAlchemy
    id = db.Column(db.Integer, primary_key=True)
    emailAddress = db.Column(db.String(100), unique=True)
    name = db.Column(db.String(1000))
    password = db.Column(db.String(100))
    zipcode = db.Column(db.String, nullable=False)
    userImage = db.Column(db.String(1000))
    hiking = db.Column(db.Boolean, default=False, nullable=False)
    mountainBiking = db.Column(db.Boolean, default=False, nullable=False)
    camping = db.Column(db.Boolean, default=False, nullable=False)
