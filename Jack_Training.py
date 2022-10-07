from math import sqrt
import LinearRegression as LinearRegression
import sklearn
import pandas
import matplotlib
import xlrd
import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt

#from sklearn.linear_model import LinearRegression

# df = pd.read_excel('F:\pythonprojects\dataset_order_picking.xlsx')
#df = pd.read_csv('F:\\Energie\\buffervat-dec-2021-geleverd.csv')
#df = pd.read_csv('F:\Energie\energiemeter-jan-dag-2022.csv')
from sklearn.metrics import mean_squared_error

df = pd.read_excel('F:\Energie\energiemeter-jan-dag-2022.xlsx')
#print(df)

y = df['ELECTOTVERBRUIKT']
X = df.drop(['DATE', 'ELECTOTVERBRUIKT', 'ELECTOTGELEVERD'], axis=1)
#df = pd.get_dummies(df, columns=['ELECTOTVERBRUIKT', 'ELECTOTGELEVERD'], drop_first=True)
#df = pd.get_dummies(df, columns=['ELECTOTGELEVERD'], drop_first=True)
print(df)
from sklearn.model_selection import train_test_split
X, y = pd.arange(10).reshape((5, 2)), range(5)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

from sklearn.linear_model import LinearRegression
model = LinearRegression().fit(X_train, y_train)
# y_train_score = model.predict(X_train)
# y_test_score = model.predict(X_test)

# print('Train data:')
# print('RSME = ' + str(sqrt(mean_squared_error(y_train, y_train_score))))
# print('R^2 = ' + str(LinearRegression.r2_score(y_train, y_train_score)))
#
# print('Test data:')
# print('RSME = ' + str(sqrt(mean_squared_error(y_test, y_test_score))))
# print('R^2 = ' + str(LinearRegression.r2_score(y_test, y_test_score)))
#sns.pairplot(df, kind='reg')
#plt.show()
