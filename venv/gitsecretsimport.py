import os

try:
    import config
    trail_api_key = config.trail_api_key
    geo_encode_key = config.geo_encode_key
    weather_api_key = config.weather_api_key
    map_api_key = config.map_api_key
except:
    print('Missing config.py')
    

keys = {"trail_api_key": trail_api_key,
        "geo_encode_key": geo_encode_key,
        "weather_api_key": weather_api_key,
        "map_api_key": map_api_key}
