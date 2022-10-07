import time
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib import style
import numpy as np
import random
import serial
import datetime

# set up the serial line
from pyasn1.compat import string
plt.ion()
# make sure the 'COM#' is set according the Windows Device Manager
ser = serial.Serial('COM12', 9600, timeout=1)
ser.flushInput()
ser.close()
ser.open() # this will also reboot the arduino

teller = 0

# Create figure for plotting
fig = plt.figure()
ax = fig.add_subplot(1, 1, 1)
xs = [] #store trials here (n)
ys = [] #store relative frequency here
rs = [] #for theoretical probability

# # This function is called periodically from FuncAnimation
# def animate(i, xs, ys):
#
#     #Read and record the data
#     input_line = ser.readline() # read a byte string
#     line_as_list = input_line.decode().split(',')  # decode byte string into Unicode
#     print(line_as_list[0])
#     i = int(line_as_list[0])
#     relProb = line_as_list[1]
#     relProb_as_list = relProb.split('\n')
#     relProb_float = float(relProb_as_list[0])
#
#     # Add x and y to lists
#     xs.append(i)
#     ys.append(relProb_float)
#     rs.append(0.5)
#
#     # Limit x and y lists to 20 items
#     #xs = xs[-20:]
#     #ys = ys[-20:]
#
#     # Draw x and y lists
#     ax.clear()
#     ax.plot(xs, ys, label="Experimental Probability")
#     ax.plot(xs, rs, label="Theoretical Probability")
#
#     # Format plot
#     plt.xticks(rotation=45, ha='right')
#     plt.subplots_adjust(bottom=0.30)
#     plt.title('This is how I roll...')
#     plt.ylabel('Relative frequency')
#     plt.legend()
#     plt.axis([1, None, 0, 1.1]) #Use for arbitrary number of trials
#     #plt.axis([1, 100, 0, 1.1]) #Use for 100 trial demo
#
# # Set up plot to call animate() function periodically
# ani = animation.FuncAnimation(fig, animate, fargs=(xs, ys), interval=1000)
# plt.show()
# ser.close()


try:
    while True:
        line = ser.readline()  # read a byte
        if line:
            arduino = line.decode()  # convert the byte string to a unicode string
            print("arduino: ", arduino)
            #data = arduino.decode().split(',')  # decode byte string into Unicode
            data = arduino.split(',')  # decode byte string into Unicode
            alcoholSensor = data[0]
            print("alcoholSensor: ", alcoholSensor)
            smokeSensor = data[1]
            print("smokeSensor: ", smokeSensor)
            gasSensor = data[2]
            print("gasSensor: ", gasSensor)
            teller += 1
            # plt.plot(datetime.datetime.now(), int(alcoholSensor), color='blue', marker='.')
            # plt.plot(datetime.datetime.now(), int(smokeSensor), color='red', marker='.')
            # plt.plot(datetime.datetime.now(), int(gasSensor), color='green', marker='.')
            plt.plot(teller, int(alcoholSensor), color='blue', marker='.')
            plt.plot(teller, int(smokeSensor), color='red', marker='.')
            plt.plot(teller, int(gasSensor), color='green', marker='.')
            #plt.plot(teller, int(data[0]), int(data[1]), int(data[2]), 'og')
            plt.legend(['alcohol', 'smoke', 'gas'], loc='upper left')
            plt.xticks(rotation=45)
            plt.show()
            plt.pause(0.01)  # pause
except KeyboardInterrupt:
    ser.close()
    print("serial connection closed")
    plt.close()
