#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
#import thermal_zone

NUM_BUF_POINTS = 180
PLOT_INTERVAL = 1000

Data = None

import board
import adafruit_ina260
i2c = board.I2C()
ina260 = adafruit_ina260.INA260(i2c)

def get_names():
    return(['current', 'voltage', 'power'])

def get_values():
    return([float("{0:.2f}".format(ina260.current / 1000)), float("{0:.2f}".format(ina260.voltage)), float("{0:.2f}".format(ina260.power / 1000))])

def plot(i):
    global Data

    zone_names = get_names()
    zone_temps = get_values()
    print(zone_temps)
    Data = np.append(Data, np.array([zone_temps]), axis = 0)
    if i >= NUM_BUF_POINTS:
        Data = np.delete(Data, 0, axis = 0)
    
    plt.cla()
    plt.plot(Data, marker = 'x')
    plt.xlim(0, NUM_BUF_POINTS)
    plt.ylim(0.0, 10.0)
    plt.title('Current Monitor', fontsize = 14)
    plt.xlabel('Time', fontsize = 10)
    plt.ylabel('Current[A],Voltage[V],Power[W]', fontsize = 10)
    plt.tick_params(labelsize=10)
    plt.grid(True)
    plt.legend(labels = zone_names, loc = 'upper left', fontsize = 10)

def main():
    global Data

    zone_names = get_names()
    print(zone_names)

    Data = np.empty((0, len(zone_names)), float)

    fig = plt.figure(figsize=(10, 4))
    ani = animation.FuncAnimation(fig, plot, fargs = (), interval = PLOT_INTERVAL)
    plt.show()

if __name__ == "__main__":
    main()
