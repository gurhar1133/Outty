import requests
import http.client, urllib.parse
import json
import config
import sqlite3

class Recommender:
    def __init__(self, username):
        self.username = username
        self.fav_activities = self.get_activities_from_db(self.username)
        self.geo_encode_key = config.geo_encode_key
        self.trail_api_key = config.trail_api_key
        self.location = self.get_user_location(self.username)

    def get_activities_from_db(self, username):
        # returns user's activity preferences after fetching from the database
        db=sqlite3.connect('outty_database.db')
        cursor=db.cursor()
        # print("username input into rec:",username)

        if username:
            cursor.execute(f"select hikes, mountainbikes, roadbikes, camps from user_data where userID='{username}';")
            db_res = cursor.fetchall()
            print(f"result from fetch on {username}",db_res)
        
        
        if (username == None) or type(username) == str and len(db_res) == 0:
            print(f"{username} query failed, defaulting to 'explorer'")
            username = 'Explorer'
            self.username = username
            try:

                cursor.execute(f"select hikes, mountainbikes, roadbikes, camps from user_data where userID='{username}';")
                
                activity_tup = cursor.fetchall()[0]
                activities = []
                if activity_tup[0] == 1:
                    activities.append("hiking")
                if activity_tup[1] == 1:
                    activities.append("mountain biking")
                #TODO: no support for road biking yet
                #if activity_tup[2] == 1:
                    
                    # activities.append("road biking") 
                if activity_tup[3] == 1:
                    activities.append("camping")
                
                db.close()
                return activities

            except Exception:
                print("ran an exception!!!")
                cursor.execute('CREATE TABLE IF NOT EXISTS user_data(userID INTEGER unique, emailAddress VARCHAR(90),password VARCHAR(90),userImage VARCHAR(90),hikes BOOLEAN, mountainBikes BOOLEAN,roadBikes BOOLEAN,camps BOOLEAN, userLocation VARCHAR(90));')
                cursor.execute('INSERT INTO user_data(userId,emailAddress, password, userImage,hikes,mountainBikes,roadBikes,camps, userLocation) VALUES(?,?,?,?,?,?,?,?,?);',
                           (username, 'email@email.com', 'supersecret', '', 0, 1, 0, 0, '80302'))
                
                db.commit()
        # print("username after:",username)
        cursor.execute(f"select hikes, mountainbikes, roadbikes, camps from user_data where userID='{username}';")
        
            

        db_res = cursor.fetchall()
        activity_tup = db_res[0]
        activities = []
        if activity_tup[0] == 1:
            activities.append("hiking")
        if activity_tup[1] == 1:
            activities.append("mountain biking")
        #TODO: no support for road biking yet
        #if activity_tup[2] == 1:
            
            # activities.append("road biking") 
        if activity_tup[3] == 1:
            activities.append("camping")
        
        db.close()
        return activities
    
    def get_user_location(self, username):
        # fetches zip code from the database
        db=sqlite3.connect('outty_database.db')
        cursor=db.cursor()
        if self.username == None:
            username = 'Explorer'
        else: username = self.username

        cursor.execute(f"SELECT userLocation from user_data WHERE userID='{username}';")
        postal_code = cursor.fetchone()[0]
        
        db.close()
        
        return postal_code
    
    def trail_api_query(self, lat, lon, state, activity_pref):
        # lat and lon info to query trailapi
        print("inputs to trail_api_query(): ", lat, lon, state, activity_pref)
        url = "https://trailapi-trailapi.p.rapidapi.com/"

        querystring = {"q-activities_activity_type_name_eq":activity_pref,
                        "q-state_cont":state,
                        "q-country_cont":"United States",
                        "limit":"5",
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
            # print("SUCCESS: ", filtered_recs)

            return filtered_recs
        else:
            return "error fetching activity info"

    def recommend(self):
       
        activity_pref = self.fav_activities
        postal_code = self.location
        if len(activity_pref) == 0:
            self.fav_activities = ['mountain biking']
            activity_pref = self.fav_activities

        # geoencoding for hiking trails api using user's zip
        data = None
        geo_attempts = 0
        while data == None: # WRITE TESTS FOR THIS
            conn = http.client.HTTPConnection('api.positionstack.com')
            params = urllib.parse.urlencode({
                'access_key': self.geo_encode_key,
                'query': postal_code,
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
        
        state = data['data'][0]['region']
        lat = data['data'][0]['latitude']
        lon = data['data'][0]['longitude']
        
        # makes a recommendation for each activity that the user likes
        recs = [self.trail_api_query(lat, lon, state, act) for act in activity_pref]

        return recs

        

if __name__ == "__main__":
    test_rec = Recommender("user1")
    recs = test_rec.recommend()[0]

    for i, rec in enumerate(recs):
        print(f'{i}) \n', rec)
        print("-"*20)

    

