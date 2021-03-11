import requests
import http.client, urllib.parse
import json

class Recommender:
    def __init__(self, username):
        self.username = username
        self.fav_activities = self.get_activities_from_db(self.username)
        self.geo_encode_key = "ef0d3ada136341fc72ac418b5f694b82"
        self.trail_api_key = "d329f3c9f8msh19fbf65431a7e9fp1a4001jsn92981ccc7922"
        self.location = self.get_user_location(self.username)

    def get_activities_from_db(self, username):
        # make database query
        # return unique activities
        return "hiking"
    
    def get_user_location(self, username):
        # make database query? or its input in some other way?
        return ("Boulder", "Colorado")
    
    def recommend(self):
       
        #unique_activities = self.fav_activities
        activity = self.fav_activities
        city, state = self.location

        # geoencoding for hiking trails api
        data = None
        geo_attemps = 0
        while data == None: # WRITE TESTS FOR THIS
            conn = http.client.HTTPConnection('api.positionstack.com')
            params = urllib.parse.urlencode({
                'access_key': self.geo_encode_key,
                'query': city,
                'region': state,
                'limit': 1,
                })

            conn.request('GET', '/v1/forward?{}'.format(params))
            res = conn.getresponse()
            if not res.status == 200:
                print ('Error')
                #return "Error getting geo encoding info"
            else:
                data = res.read()
                data = json.loads(data.decode('utf-8'))
                if data['data'] == [[]]: 
                    data = None
                    geo_attemps += 1

        #print(geo_attemps)
        lat = data['data'][0]['latitude']
        lon = data['data'][0]['longitude']
        
        # lat and lon info to query trailapi

        url = "https://trailapi-trailapi.p.rapidapi.com/"

        querystring = {"q-activities_activity_type_name_eq":activity,
                        "q-state_cont":state,
                        "q-country_cont":"United States",
                        "limit":"15",
                        "lat":lat,
                        "lon":lon,
                        "radius":"20"
                        }

        headers = {
            'x-rapidapi-key': self.trail_api_key,
            'x-rapidapi-host': "trailapi-trailapi.p.rapidapi.com"
            }

        response = requests.request("GET", url, headers=headers, params=querystring)
        if response.ok:
            return json.loads(response.text)['places']
        else:
            return "error fetching activity info"

        

if __name__ == "__main__":
    test_rec = Recommender("user1")
    recs = test_rec.recommend()
    # for i in range(200):
    #     test_rec.recommend()
    for rec in recs:
        print("location:", rec.keys())
        print("city:", rec['city'])
        print("name:", rec['name'])
        print("num activities = ", len(rec['activities']))
        print("activity keys:", rec['activities'][0].keys())