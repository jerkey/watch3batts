#!/usr/bin/env python3

import serial
import time
import os

config=open('watch3batts.conf','r').read().splitlines()
COMMAND_UTIL=config[0] # this line should be the path to the battery communications executable
SERIAL=config[1] # this line of config file should be like /dev/ttyS2
logfile=open('watch3batts'+time.strftime('%Y%m%d%H%M%S')+'.csv','w')

def grabBatteryCsv(batteryAddress):
    command = ' '.join(['timeout 5', COMMAND_UTIL, SERIAL, batteryAddress, '--csv_status','|tr -d \'\\n\''])
    response = os.popen(command).read()
    return response.split(',')

battery1 = grabBatteryCsv('0xFF')
if (len(battery1)) != 77:
    print('battery1 read error: '+str(battery1))
    battery1 = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
battery2 = grabBatteryCsv('0xDF')
if (len(battery2)) != 77:
    print('battery2 read error: '+str(battery2))
    battery2 = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
battery3 = grabBatteryCsv('0xEF')
if (len(battery3)) != 77:
    print('battery3 read error: '+str(battery3))
    battery3 = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
cellVoltages = battery1[6:6+28]+battery2[6:6+28]+battery3[6:6+28]
print(len(cellVoltages))
print(cellVoltages)
print(min(cellVoltages))
print(max(cellVoltages))

