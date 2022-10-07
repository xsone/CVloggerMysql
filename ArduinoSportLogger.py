import serial


# import pandas as pd

# make sure the 'COM#' is set according the Windows Device Manager
ser = serial.Serial('COM9', 9600)
fileName = "sport-data.csv"  # name of the CSV file generated

# ser = serial.Serial(arduino_port, baud)
# print("Connected to Arduino port:" + ser)
file = open(fileName, "a")
print("Created file")

# display the data to the terminal
getData = str(ser.readline())
data = getData[0:][:-2]
print(data)

# add the data to the file
file = open(fileName, "a")  # append the data to the file
file.write(data)  # write data with a newline

samples = 10  # how many samples to collect
print_labels = False
line = 0  # start at 0 because our header is 0 (not real data)
while line <= samples:
    # incoming = ser.read(9999)
    # if len(incoming) > 0:
    if print_labels:
        if line == 0:
            print("Printing Column Headers")
        else:
            print("Line " + str(line) + ": writing...")
    getData = str(ser.readline())
    data = getData[0:][:-2]
    print(data)
    # plot(data)

    file = open(fileName, "a")
    file.write(data + '\n')  # write data with a newline
    line = line + 1

print("Data collection complete!")
file.close()
ser.close()
