import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn import linear_model
import statsmodels.api as sm

daily = pd.read_csv('daily.csv')
weathercode_dict = {3:'	Mainly clear, partly cloudy, and overcast',95:'Thunderstorm: Slight or moderate',45:'Fog and depositing rime fog',61:'Rain: Slight, moderate and heavy intensity',80:'Rain showers: Slight, moderate, and violent'}
#print(count(daily['weathercode']=='95' or daily['weathercode']=='96' or daily['weathercode']=='99'))
count_table = daily['weathercode'].value_counts().rename_axis('weathercodes').reset_index(name='counts')
print(count_table)
count_table = count_table.replace({"weathercodes": weathercode_dict})

print(count_table)

thunder_dataset = daily
print(thunder_dataset.head())
thunder_dataset['weathercode_nextday'] = thunder_dataset['weathercode'].shift(-1)
print(thunder_dataset)
thunder_dataset = thunder_dataset[thunder_dataset.time != '2021-11-08']
print(thunder_dataset)

def thunder (row):
    if row['weathercode_nextday'] == 95:
        return 1
    else:
        return 0

thunder_dataset['thunder_nextday'] = thunder_dataset.apply (lambda row: thunder(row), axis=1)
print(thunder_dataset)



Y = thunder_dataset['thunder_nextday']
X = thunder_dataset[['temperature_2m_max','temperature_2m_min','precipitation_sum','windspeed_10m_max']]

regr = linear_model.LinearRegression()
regr.fit(X, Y)
print(regr.score(X,Y))
print('Intercept: \n', regr.intercept_)
print('Coefficients: \n', regr.coef_)




X = sm.add_constant(X)
model = sm.OLS(Y, X).fit()


print_model = model.summary()
print(print_model)





#thunder_dataset = thunder_dataset[thunder_dataset.time != '2021-11-08']
#print(thunder_dataset.head())
