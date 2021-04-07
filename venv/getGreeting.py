from flask import Flask
import datetime


def getGreeting():
    currentTime = datetime.datetime.now()
    return getGreetingText(currentTime.hour)


def getGreetingText(hourOfDay):
    if hourOfDay < 12:
        greeting = 'Good Morning'
    elif 12 <= hourOfDay < 18:
        greeting = 'Good Afternoon'
    else:
        greeting = 'Good Evening'

    return greeting
