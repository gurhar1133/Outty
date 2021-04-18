# models.py
from flask_login import UserMixin
from __init__ import db
from datetime import datetime


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
    liked = db.relationship(
        'ActivityLike',
        foreign_keys='ActivityLike.user_id',
        backref='user', lazy='dynamic')

    def like_activity(self, activity):
        if not self.has_liked_activity(activity):
            like = ActivityLike(user_id=self.id, activity_id=activity.id,
                                date_added=datetime.utcnow())
            db.session.add(like)

    def unlike_activity(self, activity):
        if self.has_liked_activity(activity):
            ActivityLike.query.filter_by(
                user_id=self.id,
                activity_id=activity.id).delete()

    def has_liked_activity(self, activity):
        return ActivityLike.query.filter(
            ActivityLike.user_id == self.id,
            ActivityLike.activity_id == activity.id).count() > 0

    completed = db.relationship(
        'ActivityComplete',
        foreign_keys='ActivityComplete.user_id',
        backref='user', lazy='dynamic')

    def complete_activity(self, activity):
        if not self.has_completed_activity(activity):
            complete = ActivityComplete(user_id=self.id, activity_id=activity.id,
                                        date_added=datetime.utcnow())
            db.session.add(complete)

    def uncomplete_activity(self, activity):
        if self.has_completed_activity(activity):
            ActivityComplete.query.filter_by(
                user_id=self.id,
                activity_id=activity.id).delete()

    def has_completed_activity(self, activity):
        return ActivityComplete.query.filter(
            ActivityComplete.user_id == self.id,
            ActivityComplete.activity_id == activity.id).count() > 0


class ActivityLike(db.Model):
    __tablename__ = 'activity_like'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    activity_id = db.Column(db.Integer, db.ForeignKey('activity.id'))
    date_added = db.Column(db.DateTime)


class ActivityComplete(db.Model):
    __tablename__ = 'activity_complete'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    activity_id = db.Column(db.Integer, db.ForeignKey('activity.id'))
    date_added = db.Column(db.DateTime)


class Activity(db.Model):
    # primary keys are required by SQLAlchemy
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(1000), nullable=False)
    type = db.Column(db.String(1000), nullable=False)
    url = db.Column(db.String(1000))
    latitude = db.Column(db.String(1000), nullable=False)
    longitude = db.Column(db.String(1000), nullable=False)
    thumbnail = db.Column(db.String(1000))
    description = db.Column(db.String(5000))
    likes = db.relationship('ActivityLike', backref='activity', lazy='dynamic')
    completes = db.relationship(
        'ActivityComplete', backref='activity', lazy='dynamic')
