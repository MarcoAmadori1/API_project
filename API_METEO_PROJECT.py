#Importing libraries
import pandas as pd
import numpy as np
import json
import requests
from opencage.geocoder import OpenCageGeocode

#Base API URL
#Creating database for cities
capital_cities = ["Tirana","Andorra la Vella","Yerevan","Vienna","Baku","Minsk","Brussels","Sarajevo","Sofia","Zagreb","Nicosia","Prague","Copenhagen","Tallinn","Helsinki","Paris","Tbilisi","Berlin","Athens","Budapest","Reykjavik","Dublin","Rome","Nur-Sultan","Kosovo","Riga","Vaduz","Vilnius","Luxembourg","Valletta","Chisinau","Monaco","Podgorica","Amsterdam","Skopje","Oslo","Warsaw","Lisbon","Bucharest","Moscow","San Marino","Belgrade","Bratislava","Ljubljana","Madrid","Stockholm","Bern","Ankara","Kiev","London","Vatican City"]

key = "dd6e7f82498847d296af2990e7dfef4e"  # get api key from:  https://opencagedata.com
geocoder = OpenCageGeocode(key)

lat_list =[]
long_list=[]
country_list=[]
country_code_list=[]

for city in capital_cities:
    query_result = geocoder.geocode(city)
    temp_df = pd.json_normalize(query_result)
    country_list.append(temp_df['components.country'][0])
    country_code_list.append(temp_df['components.country_code'][0])
    lat_list.append(temp_df['geometry.lat'][0])
    long_list.append(temp_df['geometry.lng'][0])

results = pd.DataFrame (list(zip(country_list,country_code_list,capital_cities, lat_list, long_list)), columns = ['country','country_code','capital_cities', 'lat', 'long'])
print(results)

#Running API requests and saving as .json
#Building Pandas Dataframe from JSON files

base_url = "https://api.open-meteo.com/v1/forecast"

date_start = "2020–05–01T08:00:00” # 12:00 pm in PDT is 7:00 am in UTC"
date_end = "2020–05–31T08:00:00"
#https://api.open-meteo.com/v1/forecast?latitude=52.52&longitude=13.41&hourly=temperature_2m,relativehumidity_2m,apparent_temperature,pressure_msl,precipitation,weathercode,snow_height,cloudcover,direct_radiation,windspeed_10m,winddirection_10m&daily=weathercode,temperature_2m_max,temperature_2m_min,apparent_temperature_max,apparent_temperature_min,sunrise,sunset,precipitation_sum,precipitation_hours,windspeed_10m_max,windgusts_10m_max,winddirection_10m_dominant,shortwave_radiation_sum&timezone=Europe%2FBerlin&past_days=2
