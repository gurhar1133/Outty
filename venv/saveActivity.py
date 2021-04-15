from .models import Activity, User, user_liked_activities, user_completed_activities
from . import db
from flask_login import current_user
from datetime import datetime


def getActivityById(activityId):
    activity = Activity.query.filter_by(id=activityId).first()
    return activity


def addActivityToDatabase(activityData):

    # see if there are any activities with the same url
    activity = Activity.query.filter_by(url=activityData['url']).first()

    if activity:
        # if match found, activity is already in database, and do not need to add to database
        return
    else:
        # create new activity with data from activityData
        new_activity = Activity(
            name=activityData['name'],
            type=activityData['type'],
            url=activityData['url'],
            latitude=activityData['latitude'],
            longitude=activityData['longitude'],
            thumbnail=activityData['thumbnail'],
            description=activityData['description'])

        db.session.add(new_activity)
        db.session.commit()

    return


def getActivityIdByUrl(url):
    activity = Activity.query.filter_by(url=url).first()
    activityId = activity.id
    return activityId


def addLikedActivity(url):
    activityToAdd = Activity.query.filter_by(url=url).first()
    statement = user_liked_activities.insert().values(user_id=current_user.id,
                                                      activity_id=activityToAdd.id, date_added=datetime.utcnow())
    db.session.execute(statement)
    db.session.commit()
    return


def addCompletedActivity(url):
    activityToAdd = Activity.query.filter_by(url=url).first()
    statement = user_completed_activities.insert().values(user_id=current_user.id,
                                                          activity_id=activityToAdd.id, date_added=datetime.utcnow())
    db.session.execute(statement)
    db.session.commit()
    return
