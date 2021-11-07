# API_project
API:
https://open-meteo.com/en/docs

# Objective: 
Data collection by accessing the API from https://open-meteo.com/en/docs.

# Info about the API:
The API endpoint /v1/forecast accepts a WGS4 coordinate, a list of weather variables and responds with a JSON hourly weather forecast for 7 days.

The variables are devided in Hourly variables and Daily variables.

We have chosen the following variables for each, with a database for each one.

# Hourly variables selected
Most weather variables are given as an instantaneous value for the indicated hour.

Some variables like precipitation are calculated from the preceding hour as and average or sum.

Selected variables | Description | Unit |
-------------------| ------------| -----|
pressure_msl | Atmospheric air pressure reduced to sea level | hPa |
temperature_2m | Air temperature at 2 meters above ground | °C (°F) |
snow_height | Snow height on the ground | meters |
direct_radiation | Direct solar radiation as average of the preceding hour on the horizontal plane and the normal plane (perpendicular to the sun)| W/m² |
weathercode | The most severe weather condition on a given day | WMO code |
winddirection_10m | Wind direction at 10, 80, 120 or 180 meters above ground | ° |
precipitation | Total precipitation (rain, showers, snow) sum of the preceding hour | mm (inch) |
relativehumidity_2m | Relative humidity at 2 meters above ground | % |
windspeed_10m | Wind speed on 10 meters is the standard level. | km/h (mph, m/s, knots) |
apparent_temperature | Apparent temperature is the perceived feels-like tempertature combinding wind chill factor, realtive humidity and solar radition | °C (°F) |
cloudcover | Total cloud cover as an area fraction | % |

# Daily variables selected
Aggregations are a simple 24 hour aggregation from hourly values.

Selected variables | Description | Unit |
----------------- | -------------- | -------- |
weathercode | The most severe weather condition on a given day | WMO code |
temperature_2m_max, temperature_2m_min | Maximum and minimum daily air temperature at 2 meters above ground | °C (°F) |
apparent_temperature_max, apparent_temperature_min | Maximum and minimum dailt apparent temperature | °C (°F) |
sunset, sunset | Sun rise and set times | iso8601 |
precipitation_sum | Sum of daily precipitation | mm |
precipitation_hours | The number of hours with rain
windspeed_10m_max, windgusts_10m_max | Maximum wind speed and gusts on a day | hours |
winddirection_10m_dominant | Dominant wind direction | ° |
shortwave_radiation_sum | The sum of solar radiaion on a given day in Mega Joules | MJ/m² |


# json structure (BERLIN)
```json
{
  "latitude": 52.52,
  "longitude": 13.419,
  "elevation": 44.812,
  "generationtime_ms": 2.2119,
  "utc_offset_seconds": 0,
  "hourly": {
    "time": ["2021-08-28T00:00", "2021-08-28T01:00", "2021-08-28T02:00", ...],
    "temperature_2m": [13, 12.7, 12.7, 12.5, 12.5, 12.8, 13, 12.9, 13.3, ...]
  },
  "hourly_units": {
    "temperature_2m": "°C"
  },
  "current_weather": {
    "time": "2021-08-28T09:00",
    "temperature": 13.3,
    "weathercode": 3,
    "windspeed": 10.3,
    "winddirection": 262
  }
}
```
# Code explanation

In order to collect data, the first thing to do is to import libraries.

Note: the library OpenCageGeocode allows to convert coordinates to and from places.

```
import pandas as pd
import numpy as np
import json
import requests
from opencage.geocoder import OpenCageGeocode
```
In the list "capital_cities" 50 European cities of which data will be collected about are listed.

```
capital_cities = ["Tirana","Andorra la Vella","Yerevan","Vienna","Baku","Minsk","Brussels","Sarajevo","Sofia","Zagreb","Nicosia","Prague","Copenhagen","Tallinn","Helsinki","Paris","Tbilisi","Berlin","Athens","Budapest","Reykjavik","Dublin","Rome","Nur-Sultan","Kosovo","Riga","Vaduz","Vilnius","Luxembourg","Valletta","Chisinau","Monaco","Podgorica","Amsterdam","Skopje","Oslo","Warsaw","Lisbon","Bucharest","Moscow","San Marino","Belgrade","Bratislava","Ljubljana","Madrid","Stockholm","Bern","Ankara","Kiev","London","Vatican City"]
```

In order to access the OpenCage Geocode API, a key is needed.
```
key = "dd6e7f82498847d296af2990e7dfef4e" 
geocoder = OpenCageGeocode(key)
```
Four empty lists (of latitude, longitude, countries' name and countries' codes) are created.

These will be filled with the values got from the OpenCage Geocode API.

Then, these lists, together with the list of capital cities, are zipped into a data frame called "results".

At the end of the process, the string "Created dataframe with EU capital cities coordinates" is printed in the console.
```
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

```
In order to add in the data frame above the url related to every city, a for loop is used. 

It is needed to iterate over every city's latitude and longitude. These have to be added in the url.

The url also contains the parameter "&hourly=" (or "&dayly=", according to the dataset needed) followed by the variables of interest.

Once the iteration is done, the "results" dataframe is converted to a csv file and the string "Created API request urls" is printed in the console.

```
for x in range(len(results['lat'])):
    daily_url = 'https://api.open-meteo.com/v1/forecast?latitude=' + str(results['lat'][x]) + '&longitude=' + str(results['long'][x]) + '&daily=weathercode,temperature_2m_max,temperature_2m_min,apparent_temperature_max,apparent_temperature_min,sunrise,sunset,precipitation_sum,precipitation_hours,windspeed_10m_max,windgusts_10m_max,winddirection_10m_dominant,shortwave_radiation_sum&timezone=Europe%2FBerlin&past_days=2'
    results['daily_url'] = daily_url
    hourly_url = 'https://api.open-meteo.com/v1/forecast?latitude='+str(results['lat'][x])+'&longitude='+str(results['long'][x])+'&hourly=temperature_2m,relativehumidity_2m,apparent_temperature,pressure_msl,precipitation,weathercode,snow_height,cloudcover,direct_radiation,windspeed_10m,winddirection_10m&timezone=Europe%2FBerlin&past_days=2'
    results['hourly_url'] = hourly_url
results.to_csv('results.csv')
print("Created API request urls")
```

An empty dataframe called "df_daily_all" is created.

The first for loop iterates over the rows in "results".

The request.get function accesses the API related to each capital city got from the "url" column.

Then, a column cointaining all capital cities' names is created, so it will be possible to link the data to the city they're referred to.

The second for loop iterates over all the daily variables in the "json" file and a column is made out for each of them.

These columns are added to a new empty dataframe called "df1".

Each dataframe related to every city is appended to the "df_daily_all" dataframe with the function "df_daily_all.append".

Finally, for each column the name of the variable is assigned and the final dataframe "df_daily_all" is converted to a csv file called "daily.csv".

When this process is done, the string "Created daily dataset csv" is printed in the console.

```
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
```
The steps above are followed to get the data about daily variables.

However, the same process is used to create a data frame containing data about hourly variables for every city:

```
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
```

