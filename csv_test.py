import csv
import time

import pandas as pd
import matplotlib.pyplot as plt

#import xlrd
from sklearn.linear_model import LinearRegression
import seaborn as sns

x = []
y = []
y2 = []
tel = 0

# df = pd.read_excel('F:\\Energie\\buffervat-dec-2021-geleverd.csv')
# df.head()

with open('F:\\Energie\\buffervat-dec-2021-geleverd.csv', 'r') as csvfile:
    data = csv.reader(csvfile, delimiter=";")

    for row in data:

        print(row[0])
        print(row[1])
        x.append(row[0])
        y.append(row[1])

        tel = tel + 1
        if tel >= 200:
             break

#plt.bar(x, y, color='g', width=0.20, label="Elec")
plt.plot(x, y, color='g', linestyle='dashed', marker='o',label="ElecLev")
plt.xticks(rotation=90)
plt.xlabel('Time')
plt.ylabel('Elec Geleverd')
plt.title('Energie Opbrengst')
plt.legend()
plt.show()

# with open('F:\\Energie\\biostats.csv', 'r') as csvfile:
# df = pd.read_csv('F:\\Energie\\test.csv', sep=',')
# df.plot.bar(x=df.index, y=df.columns)
# data = pd.read_csv('F:\\Energie\\energiemeter-dec-2021.csv', sep=';', header=0, index_col=0, parse_dates=True, squeeze=True)
# data = pd.read_csv('F:\\Energie\\buffervat-dec-2021-geleverd.csv', sep=';', header=0, index_col=0, parse_dates=True, squeeze=True)
# data = pd.read_csv('F:\\Energie\\buffervat-dec-2021-2.csv', sep=';').drop_duplicates(keep='first').reset_index()
# data.to_csv('F:\\Energie\\buffervat-dec-2021-2.csv', sep=';', index=False) # you don't need to set sep in this because to_csv makes it comma delimited.
# data = data.head()
# data = pd.DataFrame(data, columns=["Time", "Eleclev"])
# #df["Time"] = pd.to_datetime(df['Time'])
# x = df['Date']
# data.plot(x="Time", y=["Eleclev", "Elecgeb"], kind="bar", figsize=(8, 8))


    # plt.xticks(rotation=45, ha='right')
    # plt.subplots_adjust(bottom=0.30)
    # plt.gcf().autofmt_xdate()
    # plt.axis([1, None, 0, 1.1])  # Use for arbitrary number of trials
    # if x != 0:
    #     print(x)
    #     data.plot(kind="bar", figsize=(8, 8))
    #     plt.show()
    #     tel = tel + 1
    # if tel >= 50:
    #     break

# with open('F:\\Energie\\buffervat1.csv', 'r') as csvfile:
#     plots = csv.reader(csvfile, delimiter=";")
#
#     for row in plots:
#         x.append(row[0])
#         y.append(row[1])
#         y2.append(row[2])
#
# plt.bar(x, y, color='b', width=0.30, label="ELEC")
# # plt.bar(x+0.2, y2, color='g', width=0.50, label="Elec")
# plt.xlabel('Time')
# plt.ylabel('Elec')
# plt.title('Electriciteit verloop')
# plt.legend()
# plt.show()
