## Outty
* Gurhar, Zach, Vidya, Sam

### Running the app locally

#### The app is containerized with docker and will require:

* Install docker: https://docs.docker.com/docker-for-mac/install/

* a file called config.py in the venv directory is necessary for managing api keys. It contains the necessary api keys:

    - trail_api_key = "XXXXXXXXXXXXXXXXXXXX" # trail api: https://rapidapi.com/trailapi/api/trailapi

    - geo_encode_key = "XXXXXXXXXXXXXXXXXXXX"  # geo encoding: (google maps geocoding)

    - weather_api_key = "XXXXXXXXXXXXXXXXXXXX" # OpenWeather api

    - map_api_key = "XXXXXXXXXXXXXXXXXXXX"  # Google Maps api

* collaborator access to notion page contains keys in 'notes page'

#### Run app through command line
* ``` cd venv ```

* ``` docker build -t flask-heroku:latest . ```

* ``` docker run -d -p 5000:5000 flask-heroku ```

* See Dockerfile for necessary configuration

* Potentially helpful link: https://medium.com/@ksashok containerise-your-python-flask-using-docker-and-deploy-it-onto-heroku-a0b48d025e43

