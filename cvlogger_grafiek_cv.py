# https://saralgyaan.com/posts/matplotlib-tutorial-in-python-chapter-1-introduction/
import datetime
from datetime import *
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import time
import mysql.connector

# plt.plot([0,1,2,3,4], label='y = x')
# plotting a line plot after changing it's width and height
f = plt.figure()
f.set_figwidth(15)
f.set_figheight(9)
plt.title('CV AAN in sec.')
plt.xlabel('Tijdstip CV AAN')
plt.ylabel('Sec. AAN')

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
week = []
dag = []
uur = []
min = []
sec = []
datum = []

waterLtr = []
elecACTgeleverd = []
elecACTverbruik = []
cvStatus = []
retourcvTemp = []

teller = 0


# def addlabels(x, y):
#     for i in range(len(x)):
#         plt.text(i, y[i], y[i])


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
        "SELECT datum, cvStatus, retourcvTemp FROM cvlogger WHERE datum >= '2022-09-01 00:00:00' AND datum <= '2022-09-30 23:59:59'")
        #"SELECT datum, cvStatus FROM cvlogger WHERE datum >= '" + datumBegin + " 00:00:00' AND datum <= '" + datumEind + " 23:59:59'")

    # db_cursor.execute("SELECT datum, waterLtr, elecACTgeleverd, elecACTverbruik FROM energiemeter WHERE datum >= '2022-06-30 06:19:03' AND datum <= '2022-07-01 23:00:00'")
    # db_cursor.execute("SELECT datum, waterLtr, elecACTgeleverd, elecACTverbruik FROM energiemeter WHERE datum >= '2022-06-30 06:19:03' AND datum <= '2022-07-01 23:00:00'")
    # query_data = "SELECT datum, waterLtr, elecACTgeleverd FROM energiemeter"
    # query_data = "SELECT datum, waterLtr, elecACTgeleverd FROM energiemeter"
    # plot_data = pd.read_sql(query_data, db_connection)
    print("Query geslaagd...")
    # for row in db_cursor.fetchmany(10): haalt 10 records op
    for row in db_cursor:
        print(row)
        # datum = row[0]
        tijd.append(row[0])
        print(tijd)
        # waterLtr = row[1]
        cvStatus.append(row[1])
        # print(waterLtr)
        # elecACTgeleverd = row[2]
        retourcvTemp.append(row[2])
        # elecACTverbruik.append(row[3])

        jaar.append(tijd[teller].year)
        maand.append(tijd[teller].month)
        week.append(tijd[teller].strftime("%V"))
        dag.append(tijd[teller].day)
        uur.append(tijd[teller].hour)
        min.append(tijd[teller].minute)
        sec.append(tijd[teller].second)
        datum.append(str(tijd[teller].year) + '-' + str(tijd[teller].month) + '-' + str(tijd[teller].day) + ' ' +
                     str(tijd[teller].hour) + ':' + str(tijd[teller].minute) + ':' + str(tijd[teller].second))
        #plt.plot(datum, retourcvTemp, label='ver', color='blue')

        if (cvStatus[teller] == 1 and timeState is True):
            tijdStart = tijd[teller]
            tijdStartInt = int(tijdStart.strftime('%H%M%S'))
            print("Tijdstart: ", tijdStart)
            timeState = False
        if (cvStatus[teller] == 0 and timeState is False):
            tijdStop = tijd[teller]
            tijdStopInt = int(tijdStop.strftime('%H%M%S'))
            print("Tijdstop: ", tijdStop)
            timeState = True
            tijdDiv = tijdStopInt - tijdStartInt
            print("TijdDiv: ", tijdDiv)
            tijdStart = str(tijd[teller].hour) + ':' + str(tijd[teller].minute) + ':' + str(tijd[teller].second)
            tijdStop = str(tijd[teller].hour) + ':' + str(tijd[teller].minute) + ':' + str(tijd[teller].second)
            #tijd.append(str(tijd[teller].hour) + ':' + str(tijd[teller].minute) + ':' + str(tijd[teller].second))
            datumStart = (str(tijd[teller].year) + '-' + str(tijd[teller].month) + '-' + str(tijd[teller].day) + ' ' +
                         str(tijd[teller].hour) + ':' + str(tijd[teller].minute) + ':' + str(tijd[teller].second))

            #datumStart = tijdStart + datumBegin
            if (tijdDiv > 500):
                plt.text(datumStart, tijdDiv, tijdDiv, ha='center', color='red')
                #plt.bar(datumStart, tijdDiv/10, label='ver', color='red')
                plt.bar(datumStart, tijdDiv, label='ver', color='red')
                #plt.text(datumStart, retourcvTemp, retourcvTemp, ha='center', color='blue')
                #plt.bar(datumStart, retourcvTemp, label='ver', color='blue')

            #plt.ylabel(datumStart, datumDiv)
            # calling the function to add value labels

            # plt.bar(sec, datumDiv, label='ver', color='red')
            #plt.bar(datumStart, retourcvTemp, label='ver', color='blue')

        teller = teller + 1

    # datum[0] is datetime.datetime object
    # jaar = datum[0].year
    # print("Jaar: {:04d}".format(jaar))
    # maand = datum[0].month
    # print("Maand: {:02d}".format(maand))
    # dag = datum[0].day
    # print("Dag: {:02d}".format(dag))
    # uur = datum[0].hour
    # min = datum[0].minute
    # sec = datum[0].second
    # tijdtst = datum[0].time()
    # print("Tijdtst: ", tijdtst)
    # print("Jaar: ", jaar)
    # print("Maand ", maand)
    # print("Dag: ", dag)
    # print("Uur: ", uur)
    # print("Min: ", min)
    # print("Sec: ", sec)
    # tijd = "{:02d}:{:02d}:{:02d}".format(uur, min, sec)
    # print("Tijd: {:02d}:{:02d}:{:02d}".format(uur, min, sec))

    # tijdtst = uur + ':' + min
    # print("Tijd: ", tijd)
    # print("TijdsDuur: ", tijdsDuur)

    # print("Tijd: ", uur)
    # print("Datum: ", datum)
    # print("Water: ", waterLtr)
    # print("ElecGel: ", elecACTgeleverd)
    # print("ElecVer: ", elecACTverbruik)
    # print("cvStatus: ", cvStatus)

    # Visualizing Data using Matplotlib
    # figure, axes = plt.subplots(figsize=(10, 6))
    # axes.xaxis.set_major_formatter(mdates.DateFormatter('%H-%M-%S'))
    # plt.plot(datum, waterLtr)
    # plt.bar(dag, elecACTgeleverd)
    # plt.bar(tijd, elecACTgeleverd, label='lev', color='green')
    # plt.bar(tijd, elecACTverbruik, label='ver', color='red')
    # plt.bar(uur, elecACTgeleverd, label='lev', color='green')
    # plt.bar(uur, elecACTverbruik, label='ver', color='red')
    # plt.bar(uur, waterLtr, label='water', color='blue')
    # plt.ylim(0, 4500)
    # plt.bar(datumStart, cvStatus, label='ver', color='red')
    # plt.bar(datumStop, cvStatus)
    # plt.bar(tijd, tijdsDuur, label='ver', color='red')
    # plt.bar(tijd, tijdsDuur, label='ver', color='red')

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

# db_cursor.execute("select * from energiemeter")
# db_cursor.execute("SELECT date, elecTOTgeleverd, elecACTgeleverd FROM energiemeter")

#     query = "SELECT date, elecTOTgeleverd, elecACTgeleverd FROM energiemeter"
#     result_data = pd.read_sql(query, db_connection)
# except Exception as e:
#     db_connection.close()
#     print(str(e))
#
#
# plots = result_data
# for row in plots:
#     print(x, y)
#     if row == 10:
#        break
#     x.append(row[0])
#     y.append(row[1])
# plt.plot(x, y, marker='o')
# plt.title('Data van Energielogger MySQL-DB')
# plt.xlabel('Time')
# plt.ylabel('EnergieGeleverd')
# plt.show()

"""
def time_to_int(dateobj):
    total = int(dateobj.strftime('%S'))
    total += int(dateobj.strftime('%M')) * 60
    total += int(dateobj.strftime('%H')) * 60 * 60
    total += (int(dateobj.strftime('%j')) - 1) * 60 * 60 * 24
    total += (int(dateobj.strftime('%Y')) - 1970) * 60 * 60 * 24 * 365
    return total



result_dataFrame.plot
result_dataFrame.to_csv('Test.csv')
result_dataFrame.info()

# maak een figuur aan en assen om op te plotten
fig, ax = plt.subplots()

# onderzoek de correlatie tussen het aantal confirmed cases en aantal sterfgevallen
ax.scatter(result_dataFrame['date'], result_dataFrame['elecACTgeleverd'])
# Grafiektitel en as-labels
ax.set_title('Bevestigde gevallen en doded COVID-19')
ax.set_xlabel('Bevestigde COVID-19 patiënten')
ax.set_ylabel('Doden met doodsoorzaak COVID-19')
#print(db_connection)
#db_cursor = db_connection.cursor()
#db_cursor.execute("select * from energiemeter")
#db_cursor.execute("SELECT date, elecTOTgeleverd, elecACTgeleverd FROM energiemeter")


result = db_cursor.fetchall()
str(result)[0:10]
print("Total number of rows in table: ", result)
print("\nPrinting each row")
for row in result:
    date = row[0]
    print("date = ", row[0], )
    elecTOTgeleverd = row[1]
    print("elecTOTgevelerd  = ", row[1])
    elecACTgeleverd = row[2]
    print("elecACTgevelerd  = ", row[2], "\n")

for row in result:
    if row == 10:
       break
    x.append(row[0])
    y.append(row[1])
    z.append(row[2])
plt.plot(x, y, z, marker='o')
plt.title('Data from the CSV File: People and Expenses')
plt.xlabel('Time')
plt.ylabel('EnergieGeleverd')
plt.show()
"""
# plt.plot(date, elecACTgeleverd, color='g', label="Actueel Geleverd")
# plt.plot(elecACTgeleverd, color='g', label="Actueel Geleverd", linestyle = 'dotted')
# plt.grid()
# plt.legend()
# plt.xlabel("Date")
# plt.ylabel("elecACTgeleverd")
# plt.title("Energie overzicht")
# plt.show()


# for x in result:
#     print(x)

# db_cursor.execute('SELECT FROM energiemeter (gas, waterLtr, elecLTverbruik, elecLTgeleverd, elecHTverbruik, elecHTgeleverd, elecTOTverbruik, elecTOTgeleverd, elecACTverbruik, elecACTgeleverd');
# rows = db_cursor.fetchall()
# str(rows)[0:200]
# print(rows)

""""
x = []
y = []

with open('F:\\Energie\\buffervat-dec-2021-geleverd.csv', 'r') as csvfile:
    plots = csv.reader(csvfile, delimiter=';')
    for row in plots:
        if row == 10:
            break
        x.append(row[0])
        y.append(row[1])
plt.plot(x,y, marker='o')
plt.title('Data from the CSV File: People and Expenses')
plt.xlabel('Time')
plt.ylabel('EnergieGeleverd')
plt.show()

ages = [12, 13, 14, 15, 16, 17, 18, 19, 20, 21]

# Male Population
male_population = [14637892, 12563775, 13165128, 13739746, 13027935, 11349449, 15020851, 10844415, 14892165, 10532278]
#Female Population
female_population = [13239415, 11716908, 12093041, 12159708, 11564358, 9868018, 12937296, 10014673, 13990570, 9446694]
#Total Population
total_population = [27877307, 24280683, 25258169, 25899454, 24592293, 21217467, 27958147, 20859088, 28882735, 19978972]

plt.plot(ages, total_population, color='b', linestyle='-', marker='.', linewidth=4, label="Total Population")
plt.plot(ages, male_population, color='g', linestyle='--', marker='o', linewidth=3, label="Male Population")
plt.plot(ages, female_population, color='r', linestyle='-', marker='^', linewidth=2, label="Female Population")
plt.bar(ages, total_population, color='b', label="Total Population")
plt.bar(ages, male_population, color='g', label="Male Population")
plt.bar(ages, female_population, color='r', label="Female Population")
plt.grid()
plt.legend()
plt.xlabel("Age")
plt.ylabel("Total Population")
plt.title("Age-wise population of India")
plt.show()
"""
