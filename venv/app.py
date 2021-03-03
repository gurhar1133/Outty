from flask import Flask
from flask import render_template

from map_api import get_map_data # could be moved into a single apis.py file, but for now
#from weather_api import get_weather_data # might be simpler to keep separate files for people to 
                                     # work separately on
app = Flask(__name__)

@app.route("/")
def index():
    # feel free to make structural changes to api call functions add parameters etc
    # as needed
    #weather_data = get_weather_data()
    map_data = get_map_data()

    return render_template("index.html", weather_data=0, map_data=map_data)

@app.route("/home")
def home():
    return render_template("index.html")

@app.route("/about")
def about():
    return render_template("about.html")
    
if __name__ == '__main__':
    app.run(debug=True)