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


def animate():
    data = pd.read_csv('F:\\Energie\\buffervat-dec-2021-geleverd.csv')
    x_values = data['Time']
    y_values = data['Elec Geleverd']
    plt.cla()
    plt.plot(x_values, y_values)
    plt.xlabel('Time')
    plt.ylabel('ElecGelvrd')
    plt.title('Infosys')
    plt.gcf().autofmt_xdate()
    plt.tight_layout()

ani = FuncAnimation(plt.gcf(), animate, 5000)

plt.tight_layout()
plt.show()