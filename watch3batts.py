#!/usr/bin/env python3

import serial
import time
import os

config=open('watch3batts.conf','r').read().splitlines()
COMMAND_UTIL=config[0] # this line should be the path to the battery communications executable
SERIAL=config[1] # this line of config file should be like /dev/ttyS2
logfile=open('watch3batts'+time.strftime('%Y%m%d%H%M%S')+'.csv','w')

def grabBatteryCsv(batteryAddress):
    command = ' '.join(['timeout 5', COMMAND_UTIL, SERIAL, '--csv_status','|tr -d \'\\n\''])
    response = os.popen(command).read()
    return response.split(',')

battery1 = grabBatteryCsv('0xFF')
print(battery1)
battery2 = grabBatteryCsv('0xDF')
print(battery2)
battery3 = grabBatteryCsv('0xEF')
print(battery3)

