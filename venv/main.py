from . import db
from flask import Blueprint, render_template, url_for, request, redirect, flash
from flask_login import login_required, current_user
from .map_api import get_map_data
from .weather_api import get_weather_data
from .getGreeting import getGreeting
from .recommend import Recommender
import config
from .zipcodeCityState import getFullStateName
from .models import User, Activity, ActivityLike, ActivityComplete
from werkzeug.security import generate_password_hash, check_password_hash
from .updateSettings import findUserToUpdate, updateEmailAddress, updateName, updatePassword, updateZipcode, updateUserRadius, updateUserImage, updateHiking, updateMountainBiking, updateCamping
from .saveActivity import addActivityToDatabase, getActivityIdByUrl

main = Blueprint('main', __name__)


@main.route('/')
def index():
    if current_user.is_authenticated:
        return redirect(url_for('main.dash'))
    else:
        return render_template('index.html')


@main.route('/dashboard')
@login_required
def dash():
    city = current_user.city
    state = current_user.state
    weather_data = get_weather_data(
        city + ', ' + getFullStateName(current_user.state))
    map_data = get_map_data()
    greeting = getGreeting()

    # username = request.args.get("username")
    username = current_user.name
    rec = Recommender(current_user)
    favs = [activity.title() for activity in rec.fav_activities]

    interests = {'hiking': current_user.hiking,
                 'mountainBiking': current_user.mountainBiking,
                 'camping': current_user.camping}

    for fav in favs:
        interests[fav] = True
        radius = 30
        recs = rec.recommend()[0]

        print("returned recs[0]: ", recs[0])

        card2 = {'title': 'Emerald Lake Hiking Trail, Estes Park', 'activity': 'Hiking',
                 'distance': 22.5, 'image': url_for('static', filename='img/estes.jpg'), 'status': ''}
        card3 = {'title': 'City of Boulder Bike Path', 'activity': 'Biking',
                 'distance': 5.3, 'image': url_for('static', filename='img/park.jpg'), 'status': ''}
        if not recs[0]['activities'][0]['thumbnail']:
            recs[0]['activities'][0]['thumbnail'] = url_for(
                'static', filename='img/noImage.jpg')

        if len(recs[0]['activities']) != 0:
            card1 = {'title': recs[0]['activities'][0]['name'],
                     'activity': recs[0]['activities'][0]['type'],
                     'distance': recs[0]['activities'][0]['distance'],
                     'image': recs[0]['activities'][0]['thumbnail'],
                     'map-embed-url': 'https://maps.google.com/maps?q=' + str(recs[0]['coords'][0]) + ", " + str(recs[0]['coords'][1]) + '&z=15&output=embed',
                     'description': recs[0]['activities'][0]['description'],
                     'directions-url': 'https://www.google.com/maps/dir/Current+Location/' + str(recs[0]['coords'][0]) + ',' + str(recs[0]['coords'][1]) + '?ref=trail-action-menu-directions',
                     'more-info-url': recs[0]['activities'][0]['url'],
                     'status': ''
                     }

        else:  # handles empty api call returned to frontend
            card1 = card2

        suggestions = [card1, card2, card3]

        addActivityToDatabase(
            {'name': recs[0]['activities'][0]['name'],
             'type': recs[0]['activities'][0]['type'],
             'url': recs[0]['activities'][0]['url'],
             'latitude': str(recs[0]['coords'][0]),
             'longitude': str(recs[0]['coords'][1]),
             'thumbnail': recs[0]['activities'][0]['thumbnail'],
             'description': recs[0]['activities'][0]['description']
             }
        )

        activityPageId = getActivityIdByUrl(recs[0]['activities'][0]['url'])
        # print(activityPageId)

        if not username:
            username = "Explorer"
    return render_template("dash.html", suggestions=suggestions, weather_data=weather_data, greeting=greeting, activityPageId=activityPageId)


@main.route('/profile')
@login_required
def profile():
    # should read from the database to display info
    likedActivitiesData = ActivityLike.query.filter_by(
        user_id=current_user.id).all()
    likedActivitiesCount = ActivityLike.query.filter_by(
        user_id=current_user.id).count()

    likedActivities = []
    for i in range(likedActivitiesCount):
        specificActivityId = likedActivitiesData[i].activity_id
        specificActivity = Activity.query.filter_by(
            id=specificActivityId).first()
        likedActivity = {'id': specificActivity.id,
                         'name': specificActivity.name,
                         'type': specificActivity.type,
                         'thumbnail': specificActivity.thumbnail,
                         'date_added': likedActivitiesData[i].date_added
                         }
        likedActivities.append(likedActivity)

    completedActivitiesData = ActivityComplete.query.filter_by(
        user_id=current_user.id).all()
    completedActivitiesCount = ActivityComplete.query.filter_by(
        user_id=current_user.id).count()

    completedActivities = []
    for i in range(completedActivitiesCount):
        specificActivityId = completedActivitiesData[i].activity_id
        specificActivity = Activity.query.filter_by(
            id=specificActivityId).first()
        completedActivity = {'id': specificActivity.id,
                             'name': specificActivity.name,
                             'type': specificActivity.type,
                             'thumbnail': specificActivity.thumbnail,
                             'date_added': completedActivitiesData[i].date_added
                             }
        completedActivities.append(completedActivity)

    return render_template('profile.html', likedActivities=likedActivities, completedActivities=completedActivities)


@main.route('/settings')
@login_required
def settings():
    # user = findUserToUpdate(current_user.emailAddress)
    # updateEmailAddress(user, "test1@gmail.com")
    # updateName(user, "test1")
    # updatePassword(user, "test3") doesnt work yet

    return render_template('settings.html')


@main.route('/activity', methods=['GET'])
@login_required
def activity():
    # get parameter from url string
    activityId = request.args.get('id')
    activity = Activity.query.filter_by(id=activityId).first()

    # get date time, can also use in the future to maybe add a comment from user?
    # if current_user.has_liked_activity(activity):
    #     activityLike = ActivityLike.query.filter_by(
    #         activity_id=activity.id, user_id=current_user.id).first()
    #     print(activityLike.date_added)

    return render_template('activity.html', activity=activity)


@main.route('/like/<int:activity_id>/<action>')
@login_required
def like_action(activity_id, action):
    activity = Activity.query.filter_by(id=activity_id).first_or_404()
    if action == 'like':
        current_user.like_activity(activity)
        db.session.commit()
        flash('Activity has been liked')
    if action == 'unlike':
        current_user.unlike_activity(activity)
        db.session.commit()
        flash('Activity has been unliked')
    return redirect(request.referrer)


@main.route('/complete/<int:activity_id>/<action>')
@login_required
def complete_action(activity_id, action):
    activity = Activity.query.filter_by(id=activity_id).first_or_404()
    if action == 'complete':
        current_user.complete_activity(activity)
        db.session.commit()
        flash('Activity has been completed')
    if action == 'uncomplete':
        current_user.uncomplete_activity(activity)
        db.session.commit()
        flash('Activity has been uncompleted')
    return redirect(request.referrer)
