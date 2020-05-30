#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import re
import subprocess
import board
import adafruit_ina260

THERMAL_PATH = '/sys/devices/virtual/thermal/'

def get_thermal_zone_paths():
    return [os.path.join(THERMAL_PATH, m.group(0)) \
        for m in [re.search('thermal_zone[0-9]', d) \
            for d in os.listdir(THERMAL_PATH)] if m]

def read_sys_value(pth):
    return(subprocess.check_output(['cat', pth]).decode('utf-8').rstrip('\n'))

def get_thermal_zone_names(zone_paths):
    return([read_sys_value(os.path.join(p, 'type')) for p in zone_paths])

def get_thermal_zone_temps(zone_paths):
    return([int(read_sys_value(os.path.join(p, 'temp'))) for p in zone_paths])

i2c = board.I2C()
ina260 = adafruit_ina260.INA260(i2c)

def get_names():
    return(['current', 'voltage', 'power'])

def get_values():
    return([float("{0:.2f}".format(ina260.current / 1000)), float("{0:.2f}".format(ina260.voltage)), float("{0:.2f}".format(ina260.power / 1000))])

def main():
    ''' Test program '''
    print(get_names())
    print(get_value())

if __name__ == "__main__":
    main()
