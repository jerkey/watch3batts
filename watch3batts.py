#!/usr/bin/env python3
#            0      1       2              3              4               5           6                                                                                                                                                              34
CSV_HEADER=['time','state','error status','energy count','coloumb count','balancing','c1','c2','c3','c4','c5','c6','c7','c8','c9','c10','c11','c12','c13','c14','c15','c16','c17','c18','c19','c20','c21','c22','c23','c24','c25','c26','c27','c28','soc1','soc2','soc3','soc4','soc5','soc6','soc7','soc8','soc9','soc10','soc11','soc12','soc13','soc14','soc15','soc16','soc17','soc18','soc19','soc20','soc21','soc22','soc23','soc24','soc25','soc26','soc27','soc28',
#            62          63     64                 65        66     67     68     69           70           71           72           73
            'io status','vbus','contactor status','current','ntc1','ntc2','ntc3','bmsld temp','bmsla temp','bmsud temp','bmsua temp','mcu temp','comm period','pack soap','pack soh']

import serial
import time
import os

badData = ['66','66','66','66','66','66','66','66','66','66','66','66','66','66','66','66','66','66','66','66','66','66','66','66','66','66','66','66','66','66','66','66','66','66','66','66','66','66','66','66','66','66','66','66','66','66','66','66','66','66','66','66','66','66','66','66','66','66','66','66','66','66','66','66','66','66','66','66','66','66','66','66','66','66','66','66','66']

config=open('watch3batts.conf','r').read().splitlines()
COMMAND_UTIL=config[0] # this line should be the path to the battery communications executable
SERIAL=config[1] # this line of config file should be like /dev/ttyS2
logfile=open('watch3batts'+time.strftime('%Y%m%d%H%M%S')+'.csv','w')

def grabBatteryCsv(batteryAddress):
    command = ' '.join(['timeout 5', COMMAND_UTIL, SERIAL, batteryAddress, '--csv_status','|tr -d \'\\n\''])
    response = os.popen(command).read()
    return response.split(',')

def getAllBatts():
    cellVoltages, allTemps = [],[]
    battery1 = grabBatteryCsv('0xFF')
    if (len(battery1)) != 77:
        print('battery1 read error: '+str(battery1))
        battery1 = badData
    battery2 = grabBatteryCsv('0xDF')
    if (len(battery2)) != 77:
        print('battery2 read error: '+str(battery2))
        battery2 = badData
    battery3 = grabBatteryCsv('0xEF')
    if (len(battery3)) != 77:
        print('battery3 read error: '+str(battery3))
        battery3 = badData
    for i in range(28):
        cellVoltages.append(float(battery1[6+i]))
    for i in range(28):
        cellVoltages.append(float(battery2[6+i]))
    for i in range(28):
        cellVoltages.append(float(battery3[6+i]))
    for i in range(8):
        allTemps.append(float(battery1[66+i]))
    for i in range(8):
        allTemps.append(float(battery2[66+i]))
    for i in range(8):
        allTemps.append(float(battery3[66+i]))
        cellTemps = allTemps[0:4] + allTemps[8:11] + allTemps[16:19]
    return cellVoltages, allTemps, cellTemps

while True:
    cellVoltages, allTemps, cellTemps = getAllBatts()
    maxCellTemp = max(cellTemps)
    if (maxCellTemp > 50):
        print("                  ntc1,  ntc2,  ntc3, bmsld, bmsla, bmsud, bmsua, mcu")
        print("battery1 temps: "+str(allTemps[0:8]))
        print("battery2 temps: "+str(allTemps[8:16]))
        print("battery3 temps: "+str(allTemps[16:24]))
    maxCellVoltage = max(cellVoltages)
    print("max cell temp: "+str(maxCellTemp)+"	"+"max cell voltage: "+str(maxCellVoltage),end='	')
    print('	Time: {}:{:02d}:{:02d}'.format(time.localtime().tm_hour,time.localtime().tm_min,time.localtime().tm_sec))
    logString = str(int(time.time()))+','+str(cellVoltages)[1:-1]+','+str(allTemps)[1:-1]
    logfile.write(logString+'\n')
    time.sleep(6)
