import json
import requests
import pandas as pd
import datetime
import re
import sqlalchemy

api_key = 'XXXXXXXX' #add your open weather api_key here
part = 'minutely, alerts' #partitions out this info of JSON request via API
weather_data_list = []
engine = sqlalchemy.create_engine('sqlite:///weather.db')

# takes JSON location, lat, lon file and iterates through each location and passes into OpenWeatherMap API.
def load_data():  
    with open('city_list_json', 'r') as fp:
        city_json = json.load(fp)
    for places in city_json:
        lat = places['lat']
        lon = places['lon']
        weather_data = requests.get(
            f'https://api.openweathermap.org/data/2.5/onecall?lat={lat}&lon={lon}&exclude={part}&appid={api_key}')
        wd = json.loads(weather_data.text)
        print(f'Loaded: {places["city"]}')
        deconstruct_json(wd, lat, lon, places['city'])
    data_frame_to_sql(weather_data_list)


# takes JSON data from load_data() and creates a dictionary of relevant information from JSON.
def deconstruct_json(wd, lat, lon, city):
    weather_data = []
    for day in wd['daily']:
        weather_dict = {}
        weather_dict['w_day'] = datetime.date.fromtimestamp(day['dt'])
        weather_dict['sunrise'] = datetime.datetime.fromtimestamp(
            day['sunrise'])
        weather_dict['sunset'] = datetime.datetime.fromtimestamp(day['sunset'])
        weather_dict['weather'] = day['weather'][0]['main'].lower()
        weather_dict['weather_desc'] = day['weather'][0]['description']
        weather_dict['lat'] = lat
        weather_dict['lon'] = lon
        weather_dict['location'] = city
        weather_data.append(weather_dict)
    weather_data_list.append(weather_data)


# Takes complete dictionary list from load_data() and then converts dictionary list into dataframe. Once formatted into a dataframe, the data is inserted into sql.
def data_frame_to_sql(weather_data_list):
    final_df = pd.DataFrame()
    w_df = pd.DataFrame()
    for locales in weather_data_list:
        w_df = pd.DataFrame.from_records(locales)
        final_df = final_df.append(w_df, ignore_index=True)
    final_df.to_sql('weather_prediction', con=engine, if_exists='replace')
