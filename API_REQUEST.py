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
print("Created dataframe with EU capital cities coordinates")

results['daily_url'] = ''
results['hourly_url'] = ''
for x in range(len(results['lat'])):
    daily_url = 'https://api.open-meteo.com/v1/forecast?latitude=' + str(results['lat'][x]) + '&longitude=' + str(results['long'][x]) + '&daily=weathercode,temperature_2m_max,temperature_2m_min,apparent_temperature_max,apparent_temperature_min,sunrise,sunset,precipitation_sum,precipitation_hours,windspeed_10m_max,windgusts_10m_max,winddirection_10m_dominant,shortwave_radiation_sum&timezone=Europe%2FBerlin&past_days=2'
    results['daily_url'][x] = daily_url
    hourly_url = 'https://api.open-meteo.com/v1/forecast?latitude='+str(results['lat'][x])+'&longitude='+str(results['long'][x])+'&hourly=temperature_2m,relativehumidity_2m,apparent_temperature,pressure_msl,precipitation,weathercode,snow_height,cloudcover,direct_radiation,windspeed_10m,winddirection_10m&timezone=Europe%2FBerlin&past_days=2'
    results['hourly_url'][x] = hourly_url
results.to_csv('results.csv')
print("Created API request urls")


#Daily data pull
df_daily_all = pd.DataFrame()

for index, row in results.iterrows():

    r = requests.get(row['daily_url'])
    json=r.json()

    cities = row['capital_cities']
    df1 = pd.DataFrame()
    for x in ['time','weathercode','temperature_2m_max','temperature_2m_min','apparent_temperature_max','apparent_temperature_min','sunrise','sunset','precipitation_sum','precipitation_hours','windspeed_10m_max','windgusts_10m_max','winddirection_10m_dominant','shortwave_radiation_sum']:
        column = pd.json_normalize(json['daily'],record_path=[x])
        df1 = pd.concat([df1, column], axis=1,ignore_index=True)

    df1['capital_cities'] = cities
    df_daily_all = df_daily_all.append(df1, ignore_index=True)

df_daily_all.columns=columns=['time','weathercode','temperature_2m_max','temperature_2m_min','apparent_temperature_max','apparent_temperature_min','sunrise','sunset','precipitation_sum','precipitation_hours','windspeed_10m_max','windgusts_10m_max','winddirection_10m_dominant','shortwave_radiation_sum','capital_cities']
df_daily_all.to_csv('daily.csv')

print("Created daily dataset csv")

#Hourly data pull
df_hourly_all = pd.DataFrame()

for index, row in results.iterrows():

    r = requests.get(row['hourly_url'])
    json=r.json()

    cities = row['capital_cities']
    df1 = pd.DataFrame()
    for x in ['time','temperature_2m','relativehumidity_2m','apparent_temperature','pressure_msl','precipitation','weathercode','snow_height','cloudcover','direct_radiation','windspeed_10m','winddirection_10m']:
        column = pd.json_normalize(json['hourly'],record_path=[x])
        df1 = pd.concat([df1, column], axis=1,ignore_index=True)

    df1['capital_cities'] = cities
    df_hourly_all = df_hourly_all.append(df1, ignore_index=True)

df_hourly_all.columns=columns=['time','temperature_2m','relativehumidity_2m','apparent_temperature','pressure_msl','precipitation','weathercode','snow_height','cloudcover','direct_radiation','windspeed_10m','winddirection_10','capital_cities']
df_hourly_all.to_csv('hourly.csv')

print("Created hourly dataset csv")
