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
    time_list = Day.values.tolist()
    time_final = [i[8:10] for i in time_list]
    plt.bar(time_final,precipitation_sum, color = "blue")
    plt.tick_params(axis='x', rotation=70)
    plt.title("Precicipation sum 12/11/2021 - 20/11/2021 | " + str(enter_city))
    plt.ylabel("precipitation (mm)")
    plt.xlabel("day")
    plt.show()
else:
    print("Input the city with the following notation: " + " 'Rome' ")
    print("This is the list of available cities: " + str(final_list_cit))