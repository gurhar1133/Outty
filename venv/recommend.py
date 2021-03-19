import requests
import http.client, urllib.parse
import json
import config

class Recommender:
    def __init__(self, username):
        self.username = username
        self.fav_activities = self.get_activities_from_db(self.username)
        self.geo_encode_key = config.geo_encode_key
        self.trail_api_key = config.trail_api_key
        self.location = self.get_user_location(self.username)

    def get_activities_from_db(self, username):
        # make database query
        # return unique activities
        return "mountain biking"
    
    def get_user_location(self, username):
        # make database query? or its input in some other way?
        return ("Boulder", "Colorado")
    
    def recommend(self):
       
        #unique_activities = self.fav_activities
        activity_pref = self.fav_activities
        city, state = self.location

        # geoencoding for hiking trails api
        data = None
        geo_attempts = 0
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
                return "Error getting geo encoding info"
            else:
                data = res.read()
                data = json.loads(data.decode('utf-8'))
                if data['data'] == [[]]: 
                    data = None
                    geo_attempts += 1
                    if geo_attempts > 10:
                        print ('Error')
                        return "Error getting geo encoding info"
        #print(geo_attemps)
        lat = data['data'][0]['latitude']
        lon = data['data'][0]['longitude']
        
        # lat and lon info to query trailapi

        url = "https://trailapi-trailapi.p.rapidapi.com/"

        querystring = {"q-activities_activity_type_name_eq":activity_pref,
                        "q-state_cont":state,
                        "q-country_cont":"United States",
                        "limit":"20",
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
                        
                        filtered_rec['activities'].append(activity)

                filtered_recs.append(filtered_rec)

            return filtered_recs
        else:
            return "error fetching activity info"

        

if __name__ == "__main__":
    test_rec = Recommender("user1")
    recs = test_rec.recommend()
    for i, rec in enumerate(recs):
        print(f'{i}) \n', rec)
        print("-"*20)
        
    # for i in range(200):
    #     test_rec.recommend()
    # for rec in recs:
    #     print("location:", rec.keys())
    #     print("city:", rec['city'])
    #     print("name:", rec['name'])
    #     print("num activities = ", len(rec['activities']))
    #     print("activity keys:", rec['activities'][0].keys())