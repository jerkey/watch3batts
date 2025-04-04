#!/usr/bin/env python3

import serial
import time
import os

config=open('watch3batts.conf','r').read().splitlines()
COMMAND_UTIL=config[0] # this line should be the path to the battery communications executable
SERIAL=config[1] # this line of config file should be like /dev/ttyS2
logfile=open('watch3batts'+time.strftime('%Y%m%d%H%M%S')+'.csv','w')

def grabBatteryCsv(batteryAddress):

