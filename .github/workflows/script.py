import os

config = f'''
trail_api_key = "{os.environ['TRAIL_API_KEY']}"
geo_encode_key = "{os.environ['GEO_ENCODE_KEY']}"
weather_api_key = "{os.environ['WEATHER_API_KEY']}"
map_api_key = "{os.environ['MAP_API_KEY']}"
'''

with open("venv/config.py", "w+") as f:
  f.write(config)
  
  
