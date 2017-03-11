#!/usr/bin/env python

# http://raspberrypi.stackexchange.com/q/51498
import os
import json
import time
import serial
import requests
from lxml import etree     
from random import randint

ser = serial.Serial(
    port='/dev/ttyACM0',
    baudrate = 115200,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
    bytesize=serial.EIGHTBITS,
    timeout=1
)

busapi = requests.get(os.getenv('BUSHEA')+str(randint(12,20)))
tree = etree.parse(busapi)
loc = tree.xpath('/arrival/headsign')
direction = tree.xpath('/arrival/direction')

while 1:
    x=ser.readline()
    if(x != ''):
        print(x)
        if "NAME=" in x:
            name = x[5:-2]
        choice = randint(1,4)
        hour = str(randint(1,12))
        minute = str(randint(10,59))
        time = hour+":"+minute+"PM"
        if(choice == 1):
            payload = {"channel": "#doorbell-test", "username": "RailFare", "text": name+" purchased rail fare at Halekauwila station at "+time, "icon_emoji": ":monorail:"}
        if(choice == 2):
            payload = {"channel": "#doorbell-test", "username": "TheBusFare", "text": name+" purchased bus fare at "+loc+" ("+direction+") at "+time, "icon_emoji": ":oncoming_bus:"}
        if(choice == 3):
            payload = {"channel": "#doorbell-test", "username": "Bikeshare", "text": name+" purchased a bikeshare ride at Diamond Head station at "+time, "icon_emoji": ":bikeshare:"}
        if "SEND" in x:
            headers = {'Content-Type':'application/json'}
            r = requests.post(os.getenv('ENDPOINT'), headers=headers, data=json.dumps(payload))
