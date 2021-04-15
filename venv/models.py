# models.py
from flask_login import UserMixin
from . import db

# many to many relationship between activity and users
# using a table as recommended in flask documentation
user_completed_activities = db.Table('user_completed_activities',
                                     db.Column('activity_id', db.Integer, db.ForeignKey(
                                         'activity.id'), primary_key=True),
                                     db.Column('user_id', db.Integer, db.ForeignKey(
                                         'user.id'), primary_key=True),
                                     db.Column('date_added', db.DateTime))

# many to many relationship between liked activities and users
# using a table as recommended in flask documentation
user_liked_activities = db.Table('user_liked_activities',
                                 db.Column('activity_id', db.Integer, db.ForeignKey(
                                     'activity.id'), primary_key=True),
                                 db.Column('user_id', db.Integer, db.ForeignKey(
                                     'user.id'), primary_key=True),
                                 db.Column('date_added', db.DateTime))


class User(UserMixin, db.Model):
    # primary keys are required by SQLAlchemy
    id = db.Column(db.Integer, primary_key=True)
    emailAddress = db.Column(db.String(100), unique=True)
    name = db.Column(db.String(1000))
    password = db.Column(db.String(100))
    zipcode = db.Column(db.String, nullable=False)
    city = db.Column(db.String, nullable=False)
    state = db.Column(db.String, nullable=False)
    userRadius = db.Column(db.Integer)
    userImage = db.Column(db.String(1000))
    hiking = db.Column(db.Boolean, default=False, nullable=False)
    mountainBiking = db.Column(db.Boolean, default=False, nullable=False)
    camping = db.Column(db.Boolean, default=False, nullable=False)
    likedActivities = db.relationship(
        "Activity", secondary=user_liked_activities)
    completedActivities = db.relationship(
        "Activity", secondary=user_completed_activities)


class Activity(db.Model):
    # primary keys are required by SQLAlchemy
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(1000), nullable=False)
    type = db.Column(db.String(1000), nullable=False)
    url = db.Column(db.String(1000))
    latitude = db.Column(db.String(1000), nullable=False)
    longitude = db.Column(db.String(1000), nullable=False)
    thumbnail = db.Column(db.String(1000))
    description = db.Column(db.String(5000)
                            )
