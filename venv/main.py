from . import db
from flask import Blueprint, render_template, url_for
from flask_login import login_required, current_user
from map_api import get_map_data
from weather_api import get_weather_data
from getGreeting import getGreeting
from recommend import Recommender

main = Blueprint('main', __name__)


@main.route('/')
def index():
    return render_template('index.html')


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
    return render_template('profile.html', name=current_user.name, suggestions=suggestions)
