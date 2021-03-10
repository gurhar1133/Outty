from flask import Flask
import datetime

def getGreeting():
    currentTime = datetime.datetime.now()
    currentTime.hour
    if currentTime.hour < 12:
        greeting = 'Good morning'
    elif 12 <= currentTime.hour < 18:
        greeting ='Good afternoon'
    else:
        greeting='Good evening'

    return greeting
