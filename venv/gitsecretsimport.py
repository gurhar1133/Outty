import os

try:
    import config
except:
    config = 0

if config == 0:
    trail_api_key = os.environ['trail_api_key']
    geo_encode_key = os.environ['geo_encode_key']
    weather_api_key = os.environ['weather_api_key']
    map_api_key = os.environ['map_api_key']

else:
    trail_api_key = config.trail_api_key
    geo_encode_key = config.geo_encode_key
    weather_api_key = config.weather_api_key
    map_api_key = config.map_api_key

keys = {"trail_api_key": trail_api_key,
        "geo_encode_key": geo_encode_key,
        "weather_api_key": weather_api_key,
        "map_api_key": map_api_key}