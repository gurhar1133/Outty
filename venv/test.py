# tests will need to be updated but should generally work the same with test Cases
import regex as re
import unittest
from flask import Flask, render_template, redirect, url_for, request, g
from weather_api import get_weather_data
from werkzeug.security import generate_password_hash,check_password_hash
from getGreeting import getGreeting
import sqlite3
# import venv.outty_database
import os
from getGreeting import getGreetingText
from updateSettings import *
from recommend import Recommender
from models import User
from __init__ import create_app,db
from flask_testing import TestCase
from gitsecretsimport import keys
# We can all use one test case class or define a few with different setUp and tearDown methods
# up to you

#class OuttyTestCase(unittest.TestCase):
class MyTest(TestCase):

    SQLALCHEMY_DATABASE_URI = "sqlite://"
    TESTING = False

    def create_app(self):
        # pass in test configuration
        return create_app()

    def tearDown(self):
        user = User.query.filter_by(emailAddress='outty_test@test.org').first()
        db.session.delete(user)
        db.session.commit()



    def setUp(self):

        user = User.query.filter_by(emailAddress='outty_test@test.org').first()


        if user:
            # if match found, user is already in database, and do not need to add to database
            return
        else:
            new_user = User(emailAddress='outty_test@test.org',
                            name='Outty TestUser',
                            #password=generate_password_hash('testing', method='sha256'),
                            password='testing',
                            zipcode='80113',
                            city='Denver',
                            state='CO',
                            userRadius='10',
                            userImage='https://avatars.githubusercontent.com/u/28833281?v=4',
                            hiking=1,
                            mountainBiking=0,
                            camping=1
                            )
            db.session.add(new_user)
            db.session.commit()
            return

    def test_sanity(self):
         self.assertEqual(True, True)

    def test_rec_construcor_input_list(self):
          #if anything other than a user object is passed in, trigger exception
          # should be flexible enough to handle Null input
          user=findUserToUpdate('outty_test@test.org')
          test_rec = Recommender(user)
          recs = test_rec.recommend()[0]
          self.assertEqual(type(recs), list)

          # but if type of constructor input is a number or something
          # other than None or string then recommender should
          # trigger an exception
    def test_rec_construcor_input(self):
          try:
              test_rec2 = Recommender(1)
              self.fail("Should trigger exception when non string inputed")
          except Exception:
              pass

          try:
              test_rec3 = Recommender([23, 2])
              self.fail("Should trigger exception when non string inputed")
          except Exception:
              pass
          try:
              test_rec4 = Recommender({"name": "id"})
              self.fail("Should trigger exception when non string inputed")
          except Exception:
              print("cool, inputs handled correctly")

    def test_bad_trail_api_inputs(self):
          #testing bad trail api query. Should be flexible?
          user=findUserToUpdate('outty_test@test.org')
          test_rec = Recommender(user)
          try:
              res = test_rec.trail_api_query(
                  "cat", "dog", 0, test_rec.fav_activities[0])
          except Exception:
              self.fail("not flexible to bad trail api inputs")

    def test_update_email(self):
      user=findUserToUpdate('outty_test@test.org')
      updateEmailAddress(user,"outty_tester@test.org")
      email = User.query.filter_by(emailAddress='outty_tester@test.org').first().emailAddress
      self.assertEqual(email,'outty_tester@test.org')
      #need to update email address for rest of tests work
      updateEmailAddress(user,"outty_test@test.org")

    def test_updateName(self):
       user=findUserToUpdate('outty_test@test.org')
       updateName(user,"Outty Testuser2")
       name = User.query.filter_by(emailAddress='outty_test@test.org').first().name
       self.assertEqual(name,'Outty Testuser2')

    def test_updateZipcode(self):
       user=findUserToUpdate('outty_test@test.org')
       updateZipcode(user,'80111')
       zip = User.query.filter_by(emailAddress='outty_test@test.org').first().zipcode
       self.assertEqual(zip,'80111')

    def test_updateUserRadius(self):
       user=findUserToUpdate('outty_test@test.org')
       updateUserRadius(user,77)
       radius = User.query.filter_by(emailAddress='outty_test@test.org').first().userRadius
       self.assertEqual(radius,77)

    def test_updateUserImage(self):
      user=findUserToUpdate('outty_test@test.org')
      updateUserImage(user,'77')
      image = User.query.filter_by(emailAddress='outty_test@test.org').first().userImage
      self.assertEqual(image,'77')

    def test_updateHiking(self):
      user=findUserToUpdate('outty_test@test.org')
      updateHiking(user,0)
      hike = User.query.filter_by(emailAddress='outty_test@test.org').first().hiking
      self.assertEqual(hike,0)

    def test_updateMountainBiking(self):
      user=findUserToUpdate('outty_test@test.org')
      updateMountainBiking(user,1)
      bike = User.query.filter_by(emailAddress='outty_test@test.org').first().mountainBiking
      self.assertEqual(bike,1)

    def test_updateupdateCamping(self):
      user=findUserToUpdate('outty_test@test.org')
      updateCamping(user,0)
      camp = User.query.filter_by(emailAddress='outty_test@test.org').first().camping
      self.assertEqual(camp,0)

    def test_weather_api(self):
      self.assertIn("°F", get_weather_data(
          'Boulder, Colorado'))

    def test_getGreeting(self):
      self.assertEqual(getGreetingText(1),
                       'Good Morning', "Wrong greeting")
      self.assertEqual(getGreetingText(
          12), 'Good Afternoon', "Wrong greeting")
      self.assertEqual(getGreetingText(
          16), 'Good Afternoon', "Wrong greeting")
      self.assertEqual(getGreetingText(18),
                       'Good Evening', "Wrong greeting")
      self.assertEqual(getGreetingText(20),
                       'Good Evening', "Wrong greeting")

# Main: Run Test Cases
if __name__ == '__main__':
    unittest.main()
