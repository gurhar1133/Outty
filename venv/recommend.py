import requests
import http.client
import urllib.parse
import json
import os
from models import Activity
from __init__ import db
from gitsecretsimport import keys
from saveActivity import addActivityToDatabase, getActivityIdByUrl

# uses trail api and geoencoding api (see api.positionstack.com)
class Recommender:
    def __init__(self, current_user):
        self.username = current_user.name
        activities = []
        if current_user.hiking:
            activities.append("hiking")
        if current_user.mountainBiking:
            activities.append("mountain biking")
        if current_user.camping:
            activities.append("camping")
        self.fav_activities = activities
        self.userRadius = current_user.userRadius
        self.location = current_user.zipcode
        self.geo_encode_key = keys["geo_encode_key"]
        # os.envronget()
        self.trail_api_key = keys["trail_api_key"]

    def trail_api_query(self, lat, lon, state, activity_pref):
        # lat and lon info to query trailapi
        print("inputs to trail_api_query(): ", lat, lon, state, activity_pref)
        url = "https://trailapi-trailapi.p.rapidapi.com/"

        querystring = {"q-activities_activity_type_name_eq": activity_pref,
                       "q-state_cont": state,
                       "q-country_cont": "United States",
                       "limit": "5",
                       "lat": lat,
                       "lon": lon,
                       "radius": self.userRadius
                       }

        headers = {
            'x-rapidapi-key': self.trail_api_key,
            'x-rapidapi-host': "trailapi-trailapi.p.rapidapi.com"
        }

        response = requests.request(
            "GET", url, headers=headers, params=querystring)
        if response.ok:
            rec_activities = json.loads(response.text)['places']

            filtered_recs = []
            for rec in rec_activities:
                filtered_rec = {}
                # print(rec['url'])
                filtered_rec['directions'] = rec['directions']
                filtered_rec['name'] = rec['name']
                filtered_rec['city'] = rec['city']
                filtered_rec['coords'] = (rec['lat'], rec['lon'])
                filtered_rec['place_desc'] = rec['description']
                filtered_rec['activities'] = []
                #filtered_rec['lat'] = rec['lat']
                #filtered_rec['lon'] = rec['lon']

                for act in rec['activities']:
                    # print("actname:", act['name'])
                    # print("act_pref:", activity_pref)
                    if act['activity_type_name'] == activity_pref:
                        activity = {}
                        activity['name'] = act['name']
                        activity['type'] = act['activity_type_name']
                        activity['url'] = act['url']
                        activity['distance'] = act['length']
                        activity['thumbnail'] = act['thumbnail']
                        activity['description'] = act['description']
                        #activity['lat'] = act['lat']

                        filtered_rec['activities'].append(activity)

                filtered_recs.append(filtered_rec)
                # print("SUCCESS: ", filtered_recs)
                addActivityToDatabase(
                    {'name': act['name'],
                     'type': act['activity_type_name'],
                     'url': act['url'],
                     'latitude': rec['lat'],
                     'longitude': rec['lon'],
                     'thumbnail': act['thumbnail'],
                     'description': act['description']
                     }
                )

            return filtered_recs
        else:
            return "error fetching activity info"

    def recommend(self):

        activity_pref = self.fav_activities
        print("activity pref: ", activity_pref)
        postal_code = self.location
        if len(activity_pref) == 0:
            self.fav_activities = ['mountain biking']
            activity_pref = self.fav_activities

        # geoencoding for hiking trails api using user's zip
        data = None
        geo_attempts = 0
        while data == None and geo_attempts < 10:  # WRITE TESTS FOR THIS??
            
            params = urllib.parse.urlencode({
                'key': keys["geo_encode_key"],
                'address': postal_code
            })

            base_url = "https://maps.googleapis.com/maps/api/geocode/json?"
            data = requests.get(base_url, params=params)
            if data.ok:
                data = data.json()
                state = data['results'][0]['address_components'][-2]['long_name']
                lat = data['results'][0]['geometry']['bounds']['northeast']['lat']
                lon = data['results'][0]['geometry']['bounds']['northeast']['lng']

            else: geo_attempts += 1

        if geo_attempts >= 10:
            return "error geoencoding"

        # while data == None:  # WRITE TESTS FOR THIS
        #     conn = http.client.HTTPConnection('api.positionstack.com')
        #     params = urllib.parse.urlencode({
        #         'access_key': self.geo_encode_key,
        #         'query': postal_code,
        #         'limit': 1,
        #     })

        #     conn.request('GET', '/v1/forward?{}'.format(params))
        #     res = conn.getresponse()
        #     if not res.status == 200:
        #         print('Error')
        #         return "Error getting geo encoding info"
        #     else:
        #         data = res.read()
        #         data = json.loads(data.decode('utf-8'))
        #         if data['data'] == [[]]:
        #             data = None
        #             geo_attempts += 1
        #             if geo_attempts > 10:
        #                 print('Error')
        #                 return "Error getting geo encoding info"

        # state = data['data'][0]['region']
        # lat = data['data'][0]['latitude']
        # lon = data['data'][0]['longitude']

        # makes a recommendation for each activity that the user likes
        # recs = [self.trail_api_query(lat, lon, state, act)
        #         for act in activity_pref]
        recs = []
        for act in activity_pref:
            recs.append(self.trail_api_query(lat, lon, state, act))
        return recs


if __name__ == "__main__":
    test_rec = Recommender("test3")
    recs = test_rec.recommend()[0]

    for i, rec in enumerate(recs):
        print(f'{i}) \n', rec)
        print("-" * 20)
