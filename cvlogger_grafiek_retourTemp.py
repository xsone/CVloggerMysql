# https://saralgyaan.com/posts/matplotlib-tutorial-in-python-chapter-1-introduction/
import datetime
from datetime import *
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import time
import mysql.connector
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

# plt.plot([0,1,2,3,4], label='y = x')
# plotting a line plot after changing it's width and height
from scipy.stats import stats
from sklearn.linear_model import LinearRegression
#Split the data into train and test dataset
from sklearn.model_selection import train_test_split


f = plt.figure()
f.set_figwidth(15)
f.set_figheight(9)
plt.title('Voorspel met AI RetourTemp CV')
plt.xlabel('Tijd')
plt.ylabel('Retour temp CV')


# plt.yticks([1,2,3,4])
# plt.legend(loc = 'best')
# plt.show()


x = []
y = []
z = []

datetime_str = "31OCT2020231032"

tijd = []
tijdStart = []
tijdStop = []
tijdVerschil = []
tijdsDuur = []
timeState = True

# dagnr = 30
# maandnr = 8
# jaarnr = 2022
# datumBegin = str(dagnr) + '-' + str(maandnr) + '-' + str(dagnr)
datumBegin = "2022-08-29"
datumEind = "2022-08-30"


jaar = []
maand = []
dag = []
uur = []
min = []
sec = []
datum = []

waterLtr = []
elecACTgeleverd = []
elecACTverbruik = []
boilerStatus = []
retourTemp = []

x = []
y = []

retourTempMin = 60.0
retourTempMax = 0.0
teller = 0


def addlabels(x, y):
    for i in range(len(x)):
        plt.text(i, y[i], y[i])


db_connection = mysql.connector.connect(
    host='192.168.178.20',
    port=3307,
    user='Arduino',
    passwd="#@Xymox123",
    db='Energielogger',
)

if db_connection:
    print("Connectie geslaagd...")
else:
    print("Connectie mislukt..")

db_cursor = db_connection.cursor()
db_cursor.execute("SHOW DATABASES")
for rows in db_cursor:
    print(rows)

# for rows in db_cursor.fetchall():
#     print("x= ", rows[0], "y= ", rows[1])
# db_cursor.execute('SELECT FROM energiemeter (gas, waterLtr, elecLTverbruik, elecLTgeleverd, elecHTverbruik, elecHTgeleverd, elecTOTverbruik, elecTOTgeleverd, elecACTverbruik, elecACTgeleverd');
# rows = db_cursor.fetchall()
# str(rows)[0:200]
# print(rows)


try:
    # db_cursor.execute("SELECT datum, waterLtr, elecACTgeleverd FROM energiemeter ")
    db_cursor.execute(
        "SELECT datum, retourTemp FROM cvlogger WHERE datum >= '2022-09-10 00:00:00' AND datum <= '2022-09-12 23:59:59'")
        #"SELECT datum, boilerStatus FROM cvlogger WHERE datum >= '" + datumBegin + " 00:00:00' AND datum <= '" + datumEind + " 23:59:59'")

    # db_cursor.execute("SELECT datum, waterLtr, elecACTgeleverd, elecACTverbruik FROM energiemeter WHERE datum >= '2022-06-30 06:19:03' AND datum <= '2022-07-01 23:00:00'")
    # db_cursor.execute("SELECT datum, waterLtr, elecACTgeleverd, elecACTverbruik FROM energiemeter WHERE datum >= '2022-06-30 06:19:03' AND datum <= '2022-07-01 23:00:00'")
    # query_data = "SELECT datum, waterLtr, elecACTgeleverd FROM energiemeter"
    # query_data = "SELECT datum, waterLtr, elecACTgeleverd FROM energiemeter"
    # plot_data = pd.read_sql(query_data, db_connection)
    print("Query geslaagd...")
    # for row in db_cursor.fetchmany(10): haalt 10 records op

    """
    Het eerste dat u hoeft te doen, is uw gegevens opsplitsen in twee arrays, X en y. 
    Elk element van X zal een datum zijn, en het overeenkomstige element van y zal de bijbehorende kwh zijn.
    X = datum[teller]
    Y = boilerTemp[teller]
    """


    for row in db_cursor:
        #print(row)
        # datum = row[0]
        tijd.append(row[0])
        #x.append(row[0])
        #print(x)
        # waterLtr = row[1]
        retourTemp.append(row[1])
        y.append(row[1])
        #print(y)
        # elecACTgeleverd = row[2]
        # elecACTgeleverd.append(row[2])
        # elecACTverbruik.append(row[3])

        jaar.append(tijd[teller].year)
        maand.append(tijd[teller].month)
        dag.append(tijd[teller].day)
        uur.append(tijd[teller].hour)
        min.append(tijd[teller].minute)
        sec.append(tijd[teller].second)
        datum.append(str(tijd[teller].year) + '-' + str(tijd[teller].month) + '-' + str(tijd[teller].day) + ' ' +
                     str(tijd[teller].hour) + ':' + str(tijd[teller].minute) + ':' + str(tijd[teller].second))

        x.append(tijd[teller].day)


        #plt.text(datumStart, tijdDiv, tijdDiv, ha='center', color='red')
        #plt.bar(datum, retourTemp, label='ver', color='red')
        #plt.plot(datum, retourTemp, label='ver', color='red')

        # if retourTemp[teller] < 26.5:
        #     print("RetourtempMin: ", retourTemp[teller], datum[teller])

        if retourTemp[teller] > 56.0:
            print("RetourtempMax: ", retourTemp[teller], datum[teller])


        #retourTempMin = retourTemp[teller]
        if retourTempMin > retourTemp[teller]:
            retourTempMin = retourTemp[teller]
        if retourTempMax < retourTemp[teller]:
            retourTempMax = retourTemp[teller]

        teller = teller + 1

    print("RetourtempMin: ", retourTempMin)
    print("RetourtempMax: ", retourTempMax)

    for row in x:
        print("x: ", x)

    for row in y:
        print("y: ", y)



    # Split the data into train and test dataset
    #x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=1 / 3, random_state=42)
    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size = 0.2, random_state =0)


    for row in x_train:
        print("x-train: ", x_train)

    for row in y_train:
        print("y-train: ", y_train)


    from sklearn.linear_model import LinearRegression


    regressorObject = LinearRegression()
    x_train = np.array(x_train).reshape(-1, 1)
    x_test = np.array(x_test).reshape(-1, 1)
    y_train = np.array(y_train).reshape(-1, 1)
    y_test = np.array(y_test).reshape(-1, 1)
    #y_train.reshape(-1, 1)

    regressorObject.fit(x_train, y_train)
    # predict the test set
    y_pred_test_data = regressorObject.predict(x_test)

    train_score = regressorObject.score(x_train, y_train)
    print("The training score of the model is: ", train_score)
    test_score = regressorObject.score(y_test, y_test)
    print("The score of the model on test data is:", test_score)


    # Visualising the Training set results in a scatter plot
    plt.scatter(x_train, y_train, color='red')
    plt.plot(x_train, regressorObject.predict(x_train), color='blue')
    plt.title('RetourTemp versus Datum (Training set)')
    plt.xlabel('Datum ')
    plt.ylabel('RetourTemp (in degrees Celcius)')
    plt.show()



    eenheid = sec

    slope, intercept, r, p, std_err = stats.linregress(eenheid, retourTemp)
    print(r)

    def myfunc(eenheid):
        return slope * eenheid + intercept

    mymodel = list(map(myfunc, eenheid))
    retourTempVoorspel = myfunc(12)
    #print(retourTempVoorspel)

    #plt.scatter(eenheid, retourTemp)
    #plt.plot(eenheid, mymodel)


    # eenheid = dag
    # slope, intercept, r, p, std_err = stats.linregress(eenheid, retourTemp)
    # print(r)
    #
    # def myfunc(eenheid):
    #      return slope * eenheid + intercept
    #
    # mymodel = list(map(myfunc, eenheid))
    # retourTempVoorspel = myfunc(12)
    # print(retourTempVoorspel)
    #
    # plt.scatter(eenheid, retourTemp)
    # plt.plot(eenheid, mymodel)
    #plt.bar(eenheid, retourTemp, label='lev', color='green')

    # plt.xlabel("Tijd")
    # plt.ylabel("Watt")
    # plt.title("Electriciteit Geleverd/Verbruik")
    # plt.xlabel("Tijd")
    # plt.ylabel("Boiler")
    # plt.title("Electriciteit Geleverd/Verbruik")
    plt.xticks(rotation=45)
    plt.show()

except Exception as e:
    print("Query mislukt...")
    print(e)

db_connection.close()
