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

###SUNSET AND SUNRISE
enter_city = input(("Enter an European capital city to get the sunrise and sunset times:"))
if enter_city in final_list_cit:
    one_city_only = df[df.capital_cities==enter_city]
    Day = one_city_only["time"]
    sunrise = one_city_only["sunrise"]
    sunset = one_city_only["sunset"]
    time_list = Day.values.tolist()
    time_final = ["Nov " + i[8:10] for i in time_list]
    sunrise_list = sunrise.values.tolist()
    sunrise_final = [n[11:16] for n in sunrise_list]
    sunset_list = sunset.values.tolist()
    sunset_final = [j[11:16] for j in sunset_list]
    plt.subplot(1,2,1)
    plt.plot(time_final,sunrise_final, color = "red", marker = "o")
    plt.subplot(1,2,2)
    plt.plot(time_final,sunset_final, color = "blue", marker = "o")
    plt.show()
else:
    print("Input the city with the following notation: " + " 'Rome' ")
    print("This is the list of available cities: " + str(final_list_cit))


#PRECIPITATION SUM/HOURS
enter_city = input(("Enter an European capital city to know the precipiation Sum and Hours:"))
if enter_city in final_list_cit:
    one_city_only = df[df.capital_cities==enter_city]
    Day = one_city_only["time"]
    precipitation_sum = one_city_only["precipitation_sum"]
    precipitation_hours = one_city_only["precipitation_hours"]
    time_list = Day.values.tolist()
    time_final = [i[8:10] for i in time_list]
    # create figure and axis objects with subplots()
    fig, ax = plt.subplots()
    # make a plot
    ax.bar(time_final,precipitation_sum, color="red")
    # set x-axis label
    ax.set_xlabel("day", fontsize=14)
    # set y-axis label
    ax.set_ylabel("precipitation(mm)", color="red", fontsize=14)
    # twin object for two different y-axis on the sample plot
    ax2 = ax.twinx()
    # make a plot with different y-axis using second axis object
    ax2.plot(time_final, precipitation_hours, color="blue", marker="o")
    ax2.set_ylabel("hours of precipitations (h)", color="blue", fontsize=14)
    plt.title("Precicipation sum 12/11/2021 - 20/11/2021 | " + str(enter_city))
    plt.show()
else:
    print("Input the city with the following notation: " + " 'Rome' ")
    print("This is the list of available cities: " + str(final_list_cit))



