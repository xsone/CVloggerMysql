# arduinoPI.py
import json
import serial
import matplotlib.pyplot as plt
import datetime
import mysql.connector

teller = 0
elecACTverbruik = 0
elecACTgeleverd = 0

plt.ion()
plt.title("Electriciteit Geleverd/Verbruik")
# plt.ylim(0, 4500)
plt.xlabel("Tijd (sec)", fontsize='14', fontstyle='italic')
plt.ylabel("Power (Watt)", fontsize='14', fontstyle='italic')
#fig, ax = plt.subplots()
#plt.axes().grid(True)

# make sure the 'COM#' is set according the Windows Device Manager
ser = serial.Serial('COM3', 9600, timeout=1)
ser.flushInput()
ser.close()
ser.open() # this will also reboot the arduino

def writeSql():
    db_connection = mysql.connector.connect(
        host='192.168.178.20',
        port=3307,
        user='Arduino',
        passwd="#@Xymox123",
        db='Energielogger',
    )
    print(db_connection)
    db_cursor = db_connection.cursor()
    db_cursor.execute("INSERT INTO buffervat (elecACTverbruik, elecACTgeleverd) VALUES(%s, %s)", (elecACTverbruik, elecACTgeleverd))
    db_connection.commit()


try:
    while True:
        line = ser.readline()  # read a byte
        if line:
            arduino = line.decode()  # convert the byte string to a unicode string
            print(arduino)
            data = json.loads(arduino)
            print("Teller: ", teller)
            teller += 1
            elecACTverbruik = data["elecACTverbruik"]
            print("Gebruik: ", elecACTverbruik)
            elecACTgeleverd = data["elecACTgeleverd"]
            print("Geleverd: ", elecACTgeleverd)
            # plt.bar(teller, elecACTgeleverd, label='lev', color='green')
            # plt.bar(teller, elecACTverbruik, label='ver', color='red')
            # plt.ylim(0, 4500)
            plt.plot(datetime.datetime.now(), int(elecACTgeleverd), color='green', marker='.')
            plt.plot(datetime.datetime.now(), int(elecACTverbruik), color='red', marker='.')
            plt.legend(['GEL', 'VER'], loc='upper left')
            plt.xticks(rotation=45)
            plt.show()
            plt.pause(0.01)  # pause
            writeSql();  #schrijf dat ook naar DB buffervat
except KeyboardInterrupt:
    ser.close()
    print("serial connection closed")
    plt.close()

"""
Voorbeeld
# python_live_plot.py

import random
from itertools import count
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

plt.style.use('fivethirtyeight')

x_values = []
y_values = []

index = count()


def animate(i):
    data = pd.read_csv('python_live_plot_data.csv')
    x_values = data['Time']
    y_values = data['Price']
    plt.cla()
    plt.plot(x_values, y_values)
    plt.xlabel('Time')
    plt.ylabel('Price')
    plt.title('Infosys')
    plt.gcf().autofmt_xdate()
    plt.tight_layout()

ani = FuncAnimation(plt.gcf(), animate, 5000)

plt.tight_layout()
plt.show()
"""
