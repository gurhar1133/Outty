# feel free to make structural changes to api call functions add parameters etc
# as needed

# might be helpful for populating the hmtl template to
# return the data in easily usable format, eg an array or object
import requests
from flask import Flask, request
from gitsecretsimport import keys


def get_weather_data(city):
    """ Make api call, and return data to populate index.html """
    API_KEY = keys["weather_api_key"]  # initialize API key here
    # call API and convert response into Python dictionary
    url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&APPID={API_KEY}'
    response = requests.get(url).json()

    # error like unknown city name, inavalid api key
    if response.get('cod') != 200:
        message = response.get('message', '')
        return f'Error getting temperature for {city.title()}. Error message = {message}'

    # get current temperature and convert it into Celsius
    current_temperature = response.get('main', {}).get('temp')

    if current_temperature:
        current_temperature_f = round(
            (current_temperature - 273.15) * 9 / 5 + 32, 1)
        return f'{int(current_temperature_f)}°F'
    else:
        return f'Error getting temperature for {city.title()}'

    return
