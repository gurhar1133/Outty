import os

try:
    import config
except:
    config = 0

if config == 0:
    trail_api_key = os.environ.get('TRAIL_API_KEY')
    geo_encode_key = os.environ.get('GEO_ENCODE_KEY')
    weather_api_key = os.environ.get('WEATHER_API_KEY')
    map_api_key = os.environ.get('MAP_API_KEY')

else:
    trail_api_key = config.trail_api_key
    geo_encode_key = config.geo_encode_key
    weather_api_key = config.weather_api_key
    map_api_key = config.map_api_key

keys = {"trail_api_key": trail_api_key,
        "geo_encode_key": geo_encode_key,
        "weather_api_key": weather_api_key,
        "map_api_key": map_api_key}