from . import db
from flask import Blueprint, render_template, url_for, request, redirect
from flask_login import login_required, current_user
from .map_api import get_map_data
from .weather_api import get_weather_data
from .getGreeting import getGreeting
from .recommend import Recommender
import config
from .zipcodeCityState import getFullStateName
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from .updateSettings import findUserToUpdate, updateEmailAddress, updateName, updatePassword, updateZipcode, updateUserRadius, updateUserImage, updateHiking, updateMountainBiking, updateCamping

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
        if not username:
            username = "Explorer"
    return render_template("dash.html", suggestions=suggestions,
                           hiking=current_user.hiking, mountainBiking=current_user.mountainBiking, camping=current_user.camping,
                           city=city, state=state, weather_data=weather_data, map_data=map_data, map_api_key=config.map_api_key,
                           username=username, greeting=greeting)


@main.route('/profile')
@login_required
def profile():
    # should read from the database to display info
    # filler cards for style

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


@main.route('/settings')
@login_required
def settings():
    # user = findUserToUpdate(current_user.emailAddress)
    # updateEmailAddress(user, "test1@gmail.com")
    # updateName(user, "test1")
    # updatePassword(user, "test3") doesnt work yet

    return render_template('settings.html')
