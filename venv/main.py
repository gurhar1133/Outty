from . import db
from flask import Blueprint, render_template, url_for, request, redirect
from flask_login import login_required, current_user
from map_api import get_map_data
from weather_api import get_weather_data
from getGreeting import getGreeting
from recommend import Recommender
import config

main = Blueprint('main', __name__)


@main.route('/')
# def index():
#     return render_template('index.html')
def index():
    city = 'Boulder'
    state = 'Colorado'
    weather_data = get_weather_data(city + ', ' + state)
    map_data = get_map_data()
    greeting = getGreeting()

    # username = request.args.get("username")
    username = current_user.name
    rec = Recommender(username)
    favs = [activity.title() for activity in rec.fav_activities]

    interests = {'Hiking': False, 'Mountain Biking': False, 'Camping': False, 'Caving': False,
                 'Trail Running': False, 'Snow Sports': False, 'ATV': False, 'Horseback Riding': False}

    for fav in favs:
        interests[fav] = True
        radius = 30
        recs = rec.recommend()[0]

        print("returned recs[0]: ", recs[0])

        card2 = {'title': 'Emerald Lake Hiking Trail, Estes Park', 'activity': 'Hiking',
                 'distance': 22.5, 'image': url_for('static', filename='img/estes.jpg'), 'status': ''}
        card3 = {'title': 'City of Boulder Bike Path', 'activity': 'Biking',
                 'distance': 5.3, 'image': url_for('static', filename='img/park.jpg'), 'status': ''}

        if len(recs[0]['activities']) != 0:  # handles empy api call returned to frontend
            card1 = {'title': recs[0]['activities'][0]['name'],
                     'activity': recs[0]['activities'][0]['type'],
                     'distance': recs[0]['activities'][0]['distance'],
                     'image': recs[0]['activities'][0]['thumbnail'],
                     'description': recs[0]['activities'][0]['description'],
                     'directions-url': 'https://www.google.com/maps/dir/Current+Location/' + str(recs[0]['coords'][0]) + ',' + str(recs[0]['coords'][1]) + '?ref=trail-action-menu-directions',
                     'more-info-url': recs[0]['activities'][0]['url'],
                     'status': ''
                     }
        else:
            card1 = card2

        suggestions = [card1, card2, card3]

        if not username:
            username = "Explorer"
    return render_template("index.html", suggestions=suggestions, interests=interests, city=city, state=state, weather_data=weather_data, map_data=map_data, map_api_key=config.map_api_key, username=username, greeting=greeting)


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
    return render_template('profile.html', email=current_user.email, name=current_user.name, suggestions=suggestions)
