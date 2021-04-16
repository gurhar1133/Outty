# tests will need to be updated but should generally work the same with test Cases

import regex as re
import unittest
import config
from venv.recommend import Recommender
from flask import Flask, render_template, redirect, url_for, request, g
import venv.main
import venv.auth
from venv.map_api import get_map_data
from venv.weather_api import get_weather_data
from venv.getGreeting import getGreeting
import sqlite3
# import venv.outty_database
import os




# We can all use one test case class or define a few with different setUp and tearDown methods
# up to you

class OuttyTestCase(unittest.TestCase):

    def setUp(self):
        # outty_database.create('test.db')
        # outty_database.addUser('test.db', 'Testuser', 'emailAddress',
        #                        'password', 'userImage', 1, 1, 0, 1, '80111')
        pass

    def tearDown(self):
        if os.path.exists('./test.db'):
            os.remove('./test.db')

    def test_sanity(self):
        self.assertEqual(True, True)

    def test_rec_construcor_input(self):
        # should be flexible enough to handle Null input
        test_rec = Recommender(None)
        recs = test_rec.recommend()[0]
        self.assertEqual(type(recs), list)
        # but if type of constructor input is a number or something
        # other than None or string then recommender should
        # trigger an exception
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

    def test_rec_on_bad_username(self):
        # if not in db, should just treat as default explorer
        test_rec = Recommender("aFakeNameNotInDb")
        recs = test_rec.recommend()[0]
        self.assertEqual(type(recs), list)

    # def test_rec_handle_empty_api_return(self):
    #     pass

    # def test_rec_slow_response(self):
    #     pass

    def test_bad_trail_api_inputs(self):
        # testing bad trail api query. Should be flexible?
        test_rec = Recommender("aFakeNameNotInDb")
        try:
            res = test_rec.trail_api_query(
                "cat", "dog", 0, test_rec.fav_activities[0])
        except Exception:
            self.fail("not flexible to bad trail api inputs")

    # def test_rec_no_db(self):
    #     pass

    # def test_rec_method_inputs(self):
    #     pass

    def test_db_insert(self):
        conn = sqlite3.connect('test.db')
        c = conn.cursor()
        for row in c.execute("select count(userId) from user_data"):
            self.assertEqual(
                row[0], 1, "Insert database function not working properly")

    def test_db_user_email(self):
        conn = sqlite3.connect('test.db')
        c = conn.cursor()
        for row in c.execute("select emailAddress from user_data where userId = 'Testuser'"):
            self.assertEqual(row[0], 'emailAddress',
                             "Issues with emailaddress in database")

    def test_db_user_pw(self):
        conn = sqlite3.connect('test.db')
        c = conn.cursor()
        for row in c.execute("select password from user_data where userId = 'Testuser'"):
            self.assertEqual(row[0], 'password',
                             "Issues with password in database")

    def test_db_user_location(self):
        conn = sqlite3.connect('test.db')
        c = conn.cursor()
        for row in c.execute("select userLocation from user_data where userId = 'Testuser'"):
            self.assertEqual(row[0], '80111', "'text' does not match expected")

    def test_db_user_activities(self):
        conn = sqlite3.connect('test.db')
        c = conn.cursor()
        for row in c.execute("select hikes, mountainBikes,roadBikes,camps from user_data where userId = 'Testuser'"):
            self.assertEqual(row, (1, 1, 0, 1),
                             "Issues with activities in database")

    def test_unique_db_user(self):
        conn = sqlite3.connect('test.db')
        c = conn.cursor()
        try:
            c.execute('INSERT INTO user_data(userId,emailAddress, password, userImage,hikes,mountainBikes,roadBikes,camps, userLocation) VALUES(?,?,?,?,?,?,?,?,?);',
                      (Testuser, 'email2@email.com', 'supersecret2', '', 0, 1, 0, 0, '80302'))
            self.fail("Should fail when trying to input existing user ID.")
        except Exception:
            pass

    # def test_profile_db_update(self):
    #     pass

    def test_weather_api(self):
        self.assertIn("°F", weather_api.get_weather_data(
            'Boulder, Colorado'))

    def test_getGreeting(self):
        self.assertEqual(getGreeting.getGreetingText(1),
                         'Good Morning', "Wrong greeting")
        self.assertEqual(getGreeting.getGreetingText(
            12), 'Good Afternoon', "Wrong greeting")
        self.assertEqual(getGreeting.getGreetingText(
            16), 'Good Afternoon', "Wrong greeting")
        self.assertEqual(getGreeting.getGreetingText(18),
                         'Good Evening', "Wrong greeting")
        self.assertEqual(getGreeting.getGreetingText(20),
                         'Good Evening', "Wrong greeting")

    # def test_likeActivity(self):
    #     pass
    #
    # def test_dislikeActivity(self):
    #     pass
    #
    # def test_completeActivity(self):
    #     pass


# Main: Run Test Cases
if __name__ == '__main__':
    unittest.main()