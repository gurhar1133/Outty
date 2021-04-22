from __init__ import db
from flask import Blueprint, render_template, url_for, request, redirect, flash
from flask_login import login_required, current_user
from weather_api import get_weather_data
from getGreeting import getGreeting
from recommend import Recommender
from zipcodeCityState import getFullStateName
from models import User, Activity, ActivityLike, ActivityComplete
from werkzeug.security import generate_password_hash, check_password_hash
from updateSettings import findUserToUpdate, updateEmailAddress, updateName, updatePassword, updateZipcode, updateUserRadius, updateUserImage, updateHiking, updateMountainBiking, updateCamping
from saveActivity import getActivityIdByUrl

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
    weather_data = get_weather_data(
        current_user.city + ', ' + getFullStateName(current_user.state))
    greeting = getGreeting()

    rec = Recommender(current_user)
    favs = [activity.title() for activity in rec.fav_activities]

    interests = {'hiking': current_user.hiking,
                 'mountainBiking': current_user.mountainBiking,
                 'camping': current_user.camping}

    for fav in favs:
        interests[fav] = True
        radius = 30
        recs = rec.recommend()
        rec0 = recs[0]

    suggestions = []

    for i in range(len(recs)):
        for j in range(len(recs[i])):
            try:
                activityId = getActivityIdByUrl(
                    recs[i][j]['activities'][0]['url'])
                card = {
                    'title': recs[i][j]['activities'][0]['name'],
                    'activity': recs[i][j]['activities'][0]['type'],
                    'image': recs[i][j]['activities'][0]['thumbnail'],
                    'id': activityId,
                }

                suggestions.append(card)

            except Exception:
                # when the api fails we need some data to send to the frontend
                intType = 'hiking'
                for interest in interests.keys():
                    if interests[interest]:
                        intType = interest
                backup_card = {
                    'title': f"Couldn't find {intType} in your area",
                    'activity': intType,
                    'image': url_for('static', filename='img/lost.jpg')
                }

    print(suggestions)
    if not suggestions:
        suggestions.append({
            'title': "Couldn't find activities in your area",
            'activity': " ",
            'image': url_for('static', filename='img/lost.jpg')
        }
        )

    return render_template("dash.html", suggestions=suggestions, weather_data=weather_data, greeting=greeting)


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
    return render_template('settings.html')


@main.route('/settings', methods=['POST'])
@login_required
def settings_post():
    updates = {'newEmail': request.form.get('emailAddress'),
               'newUsername': request.form.get('newName'),
               'oldPassword': request.form.get('oldPassword'),
               'newPassword': request.form.get('password'),
               'newPassword2': request.form.get('password2'),
               'newZipcode': request.form.get('zipcode'),
               'newUserImage': request.form.get('userImage'),
               'newUserRadius': request.form.get('userRadius'),
               'hikes': request.form.get('hiking'),
               'mountainBikes': request.form.get('mountainBiking'),
               'camps': request.form.get('camping')
               }
    if (check_password_hash(current_user.password, updates['oldPassword'])):

        if updates['newPassword'] != '':
            if updates['newPassword'] == updates['newPassword2']:
                updatePassword(current_user, updates['newPassword'])
            else:
                return render_template('settings.html', message="Please ensure that new passwords match")

        if updates['newEmail'] != None and updates['newEmail'] != '':
            updateEmailAddress(current_user, updates['newEmail'])

        if updates['newUsername'] != '':
            updateName(current_user, updates['newUsername'])

        if updates['newZipcode'] != '':
            updateZipcode(current_user, updates['newZipcode'])

        if updates['newUserImage'] != '':
            updateUserImage(current_user, updates['newUserImage'])

        if updates['newUserRadius'] != '':
            updateUserRadius(current_user, updates['newUserRadius'])
        # if the user doesnt select any activities
        if updates['mountainBikes'] == None and updates['hikes'] == None and updates['camps'] == None:
            print('no activity updates')
        else:
            if updates['camps'] == 'true':
                updateCamping(current_user, True)
            else:
                updateCamping(current_user, False)

            if updates['hikes'] == 'true':
                updateHiking(current_user, True)
            else:
                updateHiking(current_user, False)

            if updates['mountainBikes'] == 'true':
                updateMountainBiking(current_user, True)
            else:
                updateMountainBiking(current_user, False)

        print(updates)

        return redirect(url_for('main.profile'))

    else:

        return render_template('settings.html', message="Please check that you entered your password correctly")


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
