# API_project
API:
https://open-meteo.com/en/docs

# Objective: 
Data collection by accessing the API from https://open-meteo.com/en/docs.

# Info about the API:
The API endpoint /v1/forecast accepts a WGS4 coordinate, 
a list of weather variables and responds with a JSON hourly 
weather forecast for 7 days.

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
