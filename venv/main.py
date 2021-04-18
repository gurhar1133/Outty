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
from saveActivity import addActivityToDatabase, getActivityIdByUrl

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
        recs = rec.recommend()[0]
        
        if len(recs) >= 1:
            try: 
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
            except Exception:
                activityPageId = "www.google.com"
        else:
            activityPageId = "www.google.com"

# then use database to generate cards???? instead of recs then we can use the id to query!
    suggestions = []
    print("returned recs:", recs)
    for i in range(len(recs)):
        try:
            card = {
                'title': recs[i]['activities'][0]['name'],
                'activity': recs[i]['activities'][0]['type'],
                'image': recs[i]['activities'][0]['thumbnail'],
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
                'image': "data:image/jpeg;base64,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"
             }
            
            
           
            

    print(suggestions)
    if suggestions == []: suggestions.append(backup_card)
    
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

        card1 = {'title': 'Tenderfoot Mountain Trail, Summit County', 'activity': 'Hiking',
                 'distance': 2.5, 'image': url_for('static', filename='img/zimg/IMG_1851.jpeg'), 'status': ''}
        card2 = {'title': 'Emerald Lake Hiking Trail, Estes Park', 'activity': 'Hiking',
                 'distance': 22.5, 'image': url_for('static', filename='img/estes.jpg'), 'status': ''}
        card3 = {'title': 'City of Boulder Bike Path', 'activity': 'Biking',
                 'distance': 5.3, 'image': url_for('static', filename='img/park.jpg'), 'status': ''}
        suggestions = [card1, card2, card3]

        return render_template('profile.html', email=current_user.emailAddress, name=current_user.name, userImage=current_user.userImage, zipcode=current_user.zipcode,
                               city=current_user.city, state=current_user.state,
                               hiking=current_user.hiking, mountainBiking=current_user.mountainBiking, camping=current_user.camping,
                               suggestions=suggestions)
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
