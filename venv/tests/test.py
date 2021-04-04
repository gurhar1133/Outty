import sys
# Adds modules from parent directory to be imported into tests
sys.path.append('../')

import unittest
import config
from recommend import Recommender
from flask import Flask, render_template, redirect, url_for, request, g
from map_api import get_map_data
from weather_api import get_weather_data
from getGreeting import getGreeting
import sqlite3


# We can all use one test case class or define a few with different setUp and tearDown methods
# up to you
class OuttyTestCase(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_sanity(self):
        self.assertEqual(True, True)

    def test_rec_construcor_input(self):
        test_rec = Recommender(None) ## should be flexible enough to handle Null input
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
            test_rec3 = Recommender([23,2])
            self.fail("Should trigger exception when non string inputed")
        except Exception:
            pass
        try:
            test_rec4 = Recommender({"name":"id"})
            self.fail("Should trigger exception when non string inputed")
        except Exception:
            print("cool, inputs handled correctly")
            



    def test_rec_on_bad_username(self):
        test_rec = Recommender("aFakeNameNotInDb") ## if not in db, should just treat as default explorer
        recs = test_rec.recommend()[0]
        self.assertEqual(type(recs), list)

    def test_rec_handle_empty_api_return(self):
        pass


    def test_rec_slow_response(self):
        pass

    def test_individual_api_fail(self):
        pass

    def test_rec_get_activities(self):
        # if there is an error in retrieving fav activities then use hiking
        test_rec = Recommender("aFakeNameNotInDb")
        test_rec.fav_activities = []
        recs = test_rec.recommend()[0]
        self.assertEqual(type(recs), list)
        

    def test_rec_get_user_loc(self):
        pass

    def test_rec_no_db(self):
        pass

    def test_rec_method_inputs(self):
        pass
        

# Main: Run Test Cases
if __name__ == '__main__':
    unittest.main()