from flask import Flask, render_template, redirect, url_for, request

from map_api import get_map_data # could be moved into a single apis.py file, but for now
from weather_api import get_weather_data # might be simpler to keep separate files for people to
                                     # work separately on
app = Flask(__name__)

@app.route("/")
def index(username=None):
    # feel free to make structural changes to api call functions add parameters etc
    # as needed
    weather_data = get_weather_data()
    map_data = get_map_data()
    username = request.args.get("username")
    if not username:
        username="Explorer"
    return render_template("index.html", weather_data=weather_data, map_data=map_data, username=username)

@app.route("/home")
def home():
    return index()

@app.route("/about")
def about():
    return render_template("about.html")

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        return redirect(url_for('index', username=request.form['username'])) #request.form['username']
    else:
        return render_template('login.html', error=error)

if __name__ == '__main__':
    app.run(debug=True)
