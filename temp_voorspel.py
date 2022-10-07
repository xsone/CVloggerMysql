# -*- coding: utf-8 -*-
"""
Created on Wed May  1 10:57:44 2019
@author: Winston Fernandes
"""
import datetime

from neuralprophet import NeuralProphet
from scipy.stats import stats

"""
Cricket Chirps (chirps/sec for the striped ground cricket) 
Vs. 
Temperature  (temperature in degrees Fahrenheit)
"""
# Import the libraries required
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import datetime as dt

# Importing the excel data
# dataset = pd.read_excel('F:\PythonProjects\elec-geleverd-mrt-sept-2022.xls')
# dataset = pd.read_excel('F:\PythonProjects\meterstanden-mrt-sept-2022.xls')
dataset = pd.read_excel('F:\PythonProjects\elecact-sept-2022.xls')
# dataset = pd.read_csv('F:\PythonProjects\mijn-meterstanden-sept-2022.csv')
dataset['datum'] = pd.to_datetime(dataset['datum'])  # omzetten naar datetime format
dataset.tail()
print('datum: ', dataset)
dataset['datum'] = dataset['datum'].map(dt.datetime.toordinal)  # omzette naar datum_nummer t.b.v. voorspelling
dataset.tail()  # laat laatste 5 rijen in dataset zien
dataset.datum.unique()  # laat alleen de unieke datums zien
datatypes = dataset.dtypes  # laat de datatypen zien
dataset.tail()
print('datum int: ', dataset)
print(datatypes)
# plt.plot(dataset['datum'], dataset['elecLTgeleverd'])
plt.plot(dataset['datum'], dataset['elecACTgeleverd'])
plt.show()

# new_column = dataset[['datum', 'elecLTgeleverd']]
# new_column.dropna(inplace = True)
# new_column.columns = ['ds', 'y'] #dataset filteren op alleen kollom datum = x-as en elecLTgeleverd = y-as
# new_column.tail()
# print(new_column)
#
# n = NeuralProphet()
# #n = NeuralProphet().fit(new_column, freq="D")
# metrics = n.fit(new_column)
# new_column = n.make_future_dataframe(dataset, periods=30)
# forecast = n.predict(new_column)
# forecast.tail()
# # plot = n.plot(forecast)
# # plot.show()
# fig_forecast = n.plot(forecast)
# fig_components = n.plot_components(forecast)
# fig_model = n.plot_parameters()

# model = n.fit(new_column, freq='D')  #we o.b.v. trainen 5000 waarden, D laat zien op dagelijkse basis, we krijgen een gemiddelde Absolute Error van 1.74
# het betreft hier alleen nog voorbereiding, nu over naar voorspelling
# future = n.make_future_dataframe(new_column, periods=30)
# forecast = n.predict(future)
# forecast = n.predict(dataset)
# forecast.tail()
# plot = n.plot(forecast)
# plot.show()


# x = dataset.iloc[:, :-1].values
x = dataset.iloc[:, :1].values  # is kolom 1 datum
# x = dataset.iloc[:, 3].values # is kolom 3 elecLTgeleverd
print("x: ", x)
y = dataset.iloc[:, 2].values  # is kolom elecACTgeleverd
# y = dataset.iloc[:, 7].values # is kolom 7 elecTOTgeleverd
print("y: ", y)

# Visualising the Training set results in a scatter plot
# plt.plot(x, color = "blue")
# plt.plot(y, color = "orange")
# plt.scatter(x, y, color = 'green')
# plt.title('Levering electriciteit zonnepanelen (werkelijk)')
# plt.xlabel('Datum')
# plt.ylabel('Geleverde electriciteit (kWh)')
# plt.show()

# slope, intercept, r, p, std_err = stats.linregress(x, y)
# print("r: ", r)
#
# def myfunc(x):
#   return slope * x + intercept
#
# mymodel = list(map(myfunc, x))
#
# elecVoorspel = myfunc(1319)
# print("elecVoorspel:", elecVoorspel)
#
# plt.scatter(x, y)
# plt.plot(x, mymodel)
# plt.show()


# Split the data into train and test dataset
from sklearn.model_selection import train_test_split

# from sklearn.cross_validation import train_test_split
x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=1 / 3, random_state=42)

# print("x-train: ", x_train)
# print("x-test", x_test)
# print("y-train: ", y_train)
# print("y-test", y_test)

x_train = np.array(x_train).reshape(-1, 1)
x_test = np.array(x_test).reshape(-1, 1)
y_train = np.array(y_train).reshape(-1, 1)
y_test = np.array(y_test).reshape(-1, 1)
# y_train.reshape(-1, 1)
# x_predict = np.array(x_predict)

# Fitting Simple Linear regression data model to train data set
from sklearn.linear_model import LinearRegression

regressorObject = LinearRegression()
regressorObject.fit(x_train, y_train)

# predict the test set
# x_test_predict = 738216
# x_predict = [738213, 738214, 738215, 738216, 738218, 738219, 738220]
# x_predict = [x_element, 738412, 738413, 738414, 738415, 738416, 738418, 738419, 738420]

#x_predict = list(range(738411, 739000))
print("x_predict_1: ", dataset['datum'][1])
x_predict = [dataset['datum'][1] + 1, dataset['datum'][1] + 10]
print("x_predict: ", x_predict)

# for element in x_predict:
#     dateTest = datetime.date.fromordinal(element)
#     print("datum: ", dateTest)
# x_predict = np.array(x_predict).reshape(-1, 1)
# y_pred_test_data = regressorObject.predict([[x_test_predict]])
# y_predict = regressorObject.predict(x_predict)
# print("y_predict: ", y_predict)
# ordinal = 738416 # is 18-9-2022


# x_predict = [738250] # put the dates of which you want to predict kwh here
# y_predict = regressorObject.predict(x_predict)

# train_score = regressorObject.score(x_train, y_train)
# print("The training score of the model is: ", train_score)
# test_score = regressorObject.score(y_test, y_test)
# print("The score of the model on test data is:", test_score)


# Visualising the Training set results in a scatter plot
# plt.scatter(x, y, color = 'green')
# plt.title('Levering electriciteit zonnepanelen (werkelijk)')
# plt.xlabel('Datum')
# plt.ylabel('Geleverde electriciteit (kWh)')
# plt.show()

# Visualising the Training set results in a scatter plot
# plt.scatter(x_train, y_train, color = 'red')
# plt.plot(x_train, regressorObject.predict(x_train), color = 'blue')
# plt.title('Voorspel levering electriciteit zonnepanelen (Training set)')
# plt.xlabel('Datum')
# plt.ylabel('Geleverde electriciteit (kWh)')
# plt.show()

# Visualising the test set results in a scatter plot
# plt.scatter(x_test, y_test, color = 'red')
# plt.plot(x_train, regressorObject.predict(x_train), color = 'blue')
# plt.title('Voorspel levering electriciteit zonnepanelen (Test set)')
# plt.xlabel('Datum')
# plt.ylabel('Geleverde electriciteit (kWh)')
# plt.show()

# Visualising the predict set results in a scatter plot
# plt.scatter(x_predict, y_predict, color = 'orange')
plt.plot(x_train, y_train, color='blue')
plt.plot(x_predict, regressorObject.predict(x_predict), color='orange')
plt.title('Voorspel levering electriciteit zonnepanelen (Predict)')
plt.xlabel('Datum')
plt.ylabel('Verwachte Geleverde electriciteit (kWh)')
plt.show()
