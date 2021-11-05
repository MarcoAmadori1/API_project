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