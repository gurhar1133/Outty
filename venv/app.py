from flask import Flask, render_template, redirect, url_for, request

from map_api import get_map_data # could be moved into a single apis.py file, but for now
from weather_api import get_weather_data # might be simpler to keep separate files for people to
                                     # work separately on
app = Flask(__name__)

@app.route("/")
@app.route("/home")
def index(userId=None):
    # feel free to make structural changes to api call functions add parameters etc
    # as needed
    weather_data = get_weather_data()
    map_data = get_map_data()
    userId = request.args.get("userId")
    if not userId:
        userId="Explorer"
    return render_template("index.html", weather_data=weather_data, map_data=map_data, userId=userId)

@app.route("/about")
def about():
    return render_template("about.html")

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        return redirect(url_for('index',
         userId=request.form['userId'],
         password=request.form['password'],
         )) #request.form['userId']
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
         #request.form['userId']
    else:
        return render_template('signup.html', error=error)

@app.route('/profile', methods=['GET', 'POST'])
def profile():
    #should read from the database to display info
    return render_template('login.html', error=error)

if __name__ == '__main__':
    app.run(debug=True)
