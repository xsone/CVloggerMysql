import matplotlib.pyplot as plt
import numpy as np
import serial
from time import time

ser = serial.Serial('COM9', 9600, timeout=1)




# flush any junk left in the serial buffer
ser.flushInput()
# ser.reset_input_buffer() # for pyserial 3.0+
run = True

# collect the data and plot a moving frame
while run:
    ser.reset_input_buffer()
    data = ser.readline().decode().strip().split(',')
    # print(data[0])
    # print(data[1])
    # print(data[2])
    # print(data[3])
    # print(data[4])
    # print(data[5])
    #
    # sometimes the incoming data is garbage, so just 'try' to do this
    try:
        # store the entire dataset for later
        ydata.append(float(data[0]))
        timepoints.append(time() - start_time)
        current_time = timepoints[-1]

        # update the plotted data
        line1.set_xdata(timepoints)
        line1.set_ydata(ydata)

        # slide the viewing frame along
        if current_time > view_time:
            plt.xlim([current_time - view_time, current_time])

        # when time's up, kill the collect+plot loop
        if timepoints[-1] > duration: run = False

    # if the try statement throws an error, just do nothing
    except:
        pass

    # update the plot
    fig1.canvas.draw()

# plot all of the data you collected
fig2 = plt.figure()
# http://matplotlib.org/users/text_props.html
fig2.suptitle('complete data trace', fontsize='18', fontweight='bold')
plt.xlabel('time, seconds', fontsize='14', fontstyle='italic')
plt.ylabel('potential, volts', fontsize='14', fontstyle='italic')
plt.axes().grid(True)

plt.plot(timepoints, ydata, marker='o', markersize=4, linestyle='none', markerfacecolor='red')
plt.ylim(yrange)
fig2.show()

ser.close()
