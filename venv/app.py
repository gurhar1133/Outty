from flask import Flask, render_template, redirect, url_for, request, g

# could be moved into a single apis.py file, but for now
from map_api import get_map_data
# might be simpler to keep separate files for people to
from weather_api import get_weather_data
# work separately on
from getGreeting import getGreeting

from recommend import Recommender

import config
import sqlite3
import outty_database

app = Flask(__name__)


@app.route("/home")
def index(userId=None):
    # feel free to make structural changes to api call functions add parameters etc
    # as needed
    city = 'Boulder'
    state = 'Colorado'
    weather_data = get_weather_data(city + ', ' + state)
    map_data = get_map_data()
    greeting = getGreeting()
    userId = request.args.get("userId")
    if not userId:
        userId = "Explorer"
    return render_template("index.html", city=city, state=state, weather_data=weather_data, map_data=map_data, userId=userId, greeting=greeting, map_api_key=config.map_api_key)


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/")
@app.route("/dashboard")
def dash(username=None):
    city = 'Boulder'
    state = 'Colorado'
    weather_data = get_weather_data(city + ', ' + state)
    map_data = get_map_data()
    greeting = getGreeting()
    username = request.args.get("username")
    
    
    rec = Recommender(username)
    favs = [activity.title() for activity in rec.fav_activities]

    interests = {'Hiking': False, 'Mountain Biking': False, 'Camping': False, 'Caving': False,
                 'Trail Running': False, 'Snow Sports': False, 'ATV': False, 'Horseback Riding': False}

    for fav in favs:
        interests[fav] = True
    
    radius = 30
    recs = rec.recommend()[0]
    
    card1 = {'title': recs[0]['activities'][0]['name'], 
            'activity': recs[0]['activities'][0]['type'], 
            'distance': recs[0]['activities'][0]['distance'], 
            'image': recs[0]['activities'][0]['thumbnail'], 
            'description': recs[0]['activities'][0]['description'],
            'directions-url': 'https://www.google.com/maps/dir/Current+Location/' + str(recs[0]['coords'][0]) + ',' + str(recs[0]['coords'][1]) + '?ref=trail-action-menu-directions', 
            'more-info-url': recs[0]['activities'][0]['url'], 
            'status': ''
            }
    
    card2 = {'title': 'Emerald Lake Hiking Trail, Estes Park', 'activity': 'Hiking',
             'distance': 22.5, 'image': url_for('static', filename='img/estes.jpg'), 'status': ''}
    card3 = {'title': 'City of Boulder Bike Path', 'activity': 'Biking',
             'distance': 5.3, 'image': url_for('static', filename='img/park.jpg'), 'status': ''}

    suggestions = [card1, card2, card3]

    if not username:
        username = "Explorer"
    return render_template("dash.html", suggestions=suggestions, interests=interests, city=city, state=state, weather_data=weather_data, map_data=map_data, map_api_key=config.map_api_key, username=username, greeting=greeting)


@app.route("/settings")
def settings():
    return render_template("settings.html")


@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        return redirect(url_for('index',
                                userId=request.form['userId'],
                                password=request.form['password'],
                                ))  # request.form['userId']
    else:
        return render_template('login.html', error=error)


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    error = None
    
    #create/connect to database

    outty_database.create('outty_database.db')    
    db = sqlite3.connect('outty_database.db')
    cursor = db.cursor()

    if request.method == 'GET':
        return render_template('signup.html')

    if request.method == 'POST':

       # write to database
        userId = request.form['userId']
        password = request.form['password']
        emailAddress = request.form['emailAddress']
        userImage = request.form['userImage']
        userLocation = request.form['userLocation']
        hikes = 'hikes' in request.form
        mountainBikes = 'mountainBikes' in request.form
        roadBikes = 'roadBikes' in request.form
        camps = 'camps' in request.form

        cursor.execute(
            'SELECT userid from user_data where userid=?', (userId,))
        result = cursor.fetchone()

        if result:
            return 'Account already exists under this username.'

        else:
            outty_database.addUser('outty_database.db',userId,emailAddress,password,userImage,hikes,mountainBikes,roadBikes,camps,userLocation)

        return redirect(url_for('dash',
                                username=request.form['userId'],
                                # userId=request.form['userId'],
                                # password=request.form['password'],
                                ))


@app.route('/profile', methods=['GET', 'POST'])
def profile():
    # should read from the database to display info
    #filler cards for style
    card1 = {'title': 'Tenderfoot Mountain Trail, Summit County', 'activity': 'Hiking',
             'distance': 2.5, 'image': url_for('static', filename='img/zimg/IMG_1851.jpeg'), 'status': ''}
    card2 = {'title': 'Emerald Lake Hiking Trail, Estes Park', 'activity': 'Hiking',
             'distance': 22.5, 'image': url_for('static', filename='img/estes.jpg'), 'status': ''}
    card3 = {'title': 'City of Boulder Bike Path', 'activity': 'Biking',
             'distance': 5.3, 'image': url_for('static', filename='img/park.jpg'), 'status': ''}

    suggestions = [card1, card2, card3]

    return render_template("profile.html", suggestions=suggestions)


if __name__ == '__main__':
    app.run(debug=True)
