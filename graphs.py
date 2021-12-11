import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np
import pandas as pd


df = pd.read_csv("daily.csv")

#list of capitals
list_cit = list(df.capital_cities)
final_list_cit = list(dict.fromkeys(list_cit))


enter_city = input(("Enter an European capital city:"))

if enter_city in final_list_cit:
    one_city_only = df[df.capital_cities==enter_city]
        #(df.loc[df['capital_cities'].isin([enter_city])])
    Day = one_city_only["time"]
    Maximum_temperature_2m = one_city_only["temperature_2m_max"]
    Minimum_temperature_2m = one_city_only["temperature_2m_min"]
    time_list = Day.values.tolist()
    time_final = ["Nov " + i[8:10] for i in time_list]
    plt.plot(time_final, Maximum_temperature_2m, color='red', marker = 'o')
    plt.plot(time_final, Minimum_temperature_2m, color='blue', marker = 'o')
    plt.title("Max temperature vs Min temperature - " + str(enter_city))
    plt.xlabel("Date (2021)")
    plt.ylabel("Temperature (°C)")
    red_patch = mpatches.Patch(color='red', label='Max T(°C)')
    blue_patch = mpatches.Patch(color='blue', label='Min T(°C)')
    plt.legend(handles=[red_patch, blue_patch])
    plt.show()
else:
    print("Input the city with the following notation: " + " 'Rome' ")
    print("This is the list of available cities: " + str(final_list_cit))