import time
import matplotlib.pyplot as plt
import numpy as np
import serial

ser = serial.Serial('COM9', 9600, timeout=1)
time.sleep(2)

plt.ion()  # sets plot to animation mode

length = 500  # determines length of data taking session (in data points)
x = [0] * length  # create empty variable of length of test
y = [0] * length
z = [0] * length

xline, = plt.plot(x)  # sets up future lines to be modified
yline, = plt.plot(y)
zline, = plt.plot(z)

plt.ylim(50, 900)  # sets the y axis limits


for i in range(length):  # while you are taking data

    input_line = ser.readline()  # read a byte string
    if input_line:
        sep = input_line.decode().split(',')  # decode byte string into Unicode
        print(int(str(sep[0])))
        print(int(str(sep[1])))
        print(int(str(sep[2])))

    x.append(int(str(sep[0])))  # add new value as int to current list
    y.append(int(str(sep[1])))
    z.append(int(str(sep[2])))

    del x[0]
    del y[0]
    del z[0]

    xline.set_xdata(np.arange(len(x)))  # sets xdata to new list length
    yline.set_xdata(np.arange(len(y)))
    zline.set_xdata(np.arange(len(z)))

    xline.set_ydata(x)  # sets ydata to new list
    yline.set_ydata(y)
    zline.set_ydata(z)

    plt.pause(0.001)  # in seconds
    plt.draw()  # draws new plot

# rows = zip(x, y)  # combines lists together
# row_arr = np.array(rows)  # creates array from list
# np.savetxt("F:\\PythonProjects\\test_radio2.txt", row_arr)  # save data in file (load w/np.loadtxt())

ser.close()
