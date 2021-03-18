from flask import Flask, render_template, redirect, url_for, request

# could be moved into a single apis.py file, but for now
from map_api import get_map_data
# might be simpler to keep separate files for people to
from weather_api import get_weather_data
# work separately on
from getGreeting import getGreeting

from recommend import Recommender

import config

app = Flask(__name__)


@app.route("/")
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


@app.route("/dashboard")
def dash(username=None):
    city = 'Boulder'
    state = 'Colorado'
    weather_data = get_weather_data(city + ', ' + state)
    map_data = get_map_data()
    greeting = getGreeting()
    username = request.args.get("username")
    rec = Recommender(username)

    interests = {'Hiking': True, 'Mountain Biking': True, 'Camping': True, 'Caving': False,
                 'Trail Running': False, 'Snow Sports': False, 'ATV': False, 'Horseback Riding': False}
    
    radius = 30
    recs = rec.recommend()
    
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
    if request.method == 'POST':
        """
        write to database
        password = request.form['password'],
        emailAddress = request.form['emailAddress'],
        userImage = request.form['userImage'],
        hikes = request.form.get('hikes'),
        mountainBikes = request.form.get['mountainBikes'],
        roadBikes = request.form.get['roadBikes'],
        camps = request.form.get['camps'],
        userLocation = request.form['userLocation'],
        """
        return redirect(url_for('index',
                                userId=request.form['userId'],
                                ))
        # request.form['userId']
    else:
        return render_template('signup.html', error=error)


@app.route('/profile', methods=['GET', 'POST'])
def profile():
    # should read from the database to display info
    return render_template('profile.html')


if __name__ == '__main__':
    app.run(debug=True)
