#!/usr/bin/env python3
  
import sqlite3

def create(dbname):
    conn = sqlite3.connect(dbname)
    c=conn.cursor()
    c.execute('CREATE TABLE IF NOT EXISTS user_data(userID INTEGER unique, emailAddress VARCHAR(90),password VARCHAR(90),userImage VARCHAR(90),hikes BOOLEAN, mountainBikes BOOLEAN,roadBikes BOOLEAN,camps BOOLEAN, userLocation VARCHAR(90));')
    conn.commit()
    conn.close()

def addUser(dbname,userId,emailAddress,password,userImage,hikes,mountainBikes,roadBikes,camps,userLocation):
    conn = sqlite3.connect(dbname)
    c=conn.cursor()
    c.execute('INSERT INTO user_data(userId,emailAddress, password, userImage,hikes,mountainBikes,roadBikes,camps, userLocation) VALUES(?,?,?,?,?,?,?,?,?);',
                           (userId, emailAddress, password, userImage, hikes, mountainBikes, roadBikes, camps, userLocation))   
    conn.commit()
    conn.close()

def updateUserId(dbname,userId):
    conn = sqlite3.connect(dbname)
    c=conn.cursor()
    c.execute('UPDATE user_data set userId = userId where userId<>userId')
    conn.commit()
    conn.close()
