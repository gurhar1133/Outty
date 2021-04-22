### Running the app

#### The app is containerized with docker and will require:

* Install docker: https://docs.docker.com/docker-for-mac/install/

* a file called config.py in the venv directory that contains the necessary api keys

* ``` cd venv ```

* ``` docker build -t flask-heroku:latest . ```

* ``` docker run -d -p 5000:5000 flask-heroku ```

* See Dockerfile for necessary configuration

* Potentially helpful link: https://medium.com/@ksashok containerise-your-python-flask-using-docker-and-deploy-it-onto-heroku-a0b48d025e43


#### Running locally without docker

* ``` cd venv ```
* ``` python -m flask run ```