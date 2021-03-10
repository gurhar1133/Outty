from flask import Flask, render_template, redirect, url_for, request

from map_api import get_map_data # could be moved into a single apis.py file, but for now
from weather_api import get_weather_data # might be simpler to keep separate files for people to
                                     # work separately on
from getGreeting import getGreeting

app = Flask(__name__)

@app.route("/")
def index(username=None):
    # feel free to make structural changes to api call functions add parameters etc
    # as needed
    city = 'Boulder'
    state = 'Colorado'
    weather_data = get_weather_data(city+', '+state)
    map_data = get_map_data()
    greeting = getGreeting()
    username = request.args.get("username")
    if not username:
        username="Explorer"
    return render_template("index.html", city = city, state=state, weather_data=weather_data, map_data=map_data, username=username, greeting = greeting)

@app.route("/home")
def home():
    return index()

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/dashboard")
def dash(username=None):
    city = 'Boulder'
    state = 'Colorado'
    weather_data = get_weather_data(city+', '+state)
    map_data = get_map_data()
    greeting = getGreeting()
    username = request.args.get("username")
    interests = ['hiking','biking','water']
    radius = 30
    # // suggestion card information
    # // status of card- none, liked, disliked, saved
    card1 = {'title':'First and Second Flatirons Loop', 'activity':'hiking', 'distance':2.2, 'image':'', 'status':''}
    card2 = {'title':'Emerald Lake Hiking Trail, Estes Park', 'activity':'hiking', 'distance':22.5, 'image':'', 'status':''}
    card3 = {'title':'City of Boulder Bike Path', 'activity':'biking', 'distance':5.3, 'image':'', 'status':''}

    suggestions=[card1,card2,card3]

    if not username:
        username="Explorer"
    return render_template("dash.html", suggestions = suggestions, interests=interests, city = city, state=state, weather_data=weather_data, map_data=map_data, username=username, greeting = greeting)

@app.route("/settings")
def settings():
    return render_template("settings.html")


@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        return redirect(url_for('index', username=request.form['username'])) #request.form['username']
    else:
        return render_template('login.html', error=error)

if __name__ == '__main__':
    app.run(debug=True)
