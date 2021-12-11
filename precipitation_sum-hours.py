import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np
import pandas as pd
import datetime

df = pd.read_csv("daily.csv")
#list of capitals
list_cit = list(df.capital_cities)
final_list_cit = list(dict.fromkeys(list_cit))

enter_city = input(("Enter an European capital city:"))
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