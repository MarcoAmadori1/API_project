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


for x in range(len(results['lat'])):
    url = 'https://api.open-meteo.com/v1/forecast?latitude=' + str(results['lat'][x]) + '&longitude=' + str(results['long'][x]) + '&daily=weathercode,temperature_2m_max,temperature_2m_min,apparent_temperature_max,apparent_temperature_min,sunrise,sunset,precipitation_sum,precipitation_hours,windspeed_10m_max,windgusts_10m_max,winddirection_10m_dominant,shortwave_radiation_sum&timezone=Europe%2FBerlin&past_days=2'
    results['url'] = url

results.to_csv('results.csv')

df_all = pd.DataFrame()

for index, row in results.iterrows():

    r = requests.get(row['url'])
    json=r.json()

    country = row['country']
    df1 = pd.DataFrame()
    for x in ['time','weathercode','temperature_2m_max','temperature_2m_min','apparent_temperature_max','apparent_temperature_min','sunrise','sunset','precipitation_sum','precipitation_hours','windspeed_10m_max','windgusts_10m_max','winddirection_10m_dominant','shortwave_radiation_sum']:
        column = pd.json_normalize(json['daily'],record_path=[x])
        df1 = pd.concat([df1, column], axis=1,ignore_index=True)

    df1['country'] = country
    df_all = df_all.append(df1, ignore_index=True)

df_all.columns=columns=['time','weathercode','temperature_2m_max','temperature_2m_min','apparent_temperature_max','apparent_temperature_min','sunrise','sunset','precipitation_sum','precipitation_hours','windspeed_10m_max','windgusts_10m_max','winddirection_10m_dominant','shortwave_radiation_sum','country']
df_all.to_csv('daily.csv')