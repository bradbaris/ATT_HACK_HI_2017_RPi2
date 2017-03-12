#!/usr/bin/env python

# http://raspberrypi.stackexchange.com/q/51498
import os
import json
import time
import serial
import random
import requests
import xml.etree.ElementTree as ET   
from random import randint

ser = serial.Serial(
    port='/dev/ttyACM0',
    baudrate = 115200,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
    bytesize=serial.EIGHTBITS,
    timeout=1
)

busNum = [12,13,14,15,16,17,18,19,20,22,23,24,26,27,28,29,30,31,33,34,35,36,37,38,39,40,41,43,44,45,46,47,48,49,50]
name = "User"

while 1:
    x=ser.readline()
    if(x != ''):
        print(x)
        if "NAME=" in x:
            name = x[5:-2]
            randBus = str(random.choice(busNum))
            busApi = requests.get("http://api.thebus.org/arrivals/", params=[('key', os.getenv('BUSHEA')),('stop', randBus)])
            root = ET.fromstring(busApi.text)
            headSign = root[randint(2,25)][3].text
            direction = root[2][5].text
            hour = str(randint(1,12))
            minute = str(randint(10,59))
            time = hour+":"+minute+"PM"

            choice = randint(1,4)
            if(choice == 1):
                payload = {"channel": "#doorbell-test", "username": "RailFare", "text": name+" purchased rail fare at '"+headSign+"' station at "+time, "icon_emoji": ":monorail:"}
            if(choice == 2):
                payload = {"channel": "#doorbell-test", "username": "TheBusFare", "text": name+" purchased bus fare at '"+headSign+"' ("+direction+") at "+time, "icon_emoji": ":oncoming_bus:"}
            if(choice == 3 or choice == 4):
                payload = {"channel": "#doorbell-test", "username": "Bikeshare", "text": name+" purchased a bikeshare ride at '"+headSign+"' at "+time, "icon_emoji": ":bikeshare:"}
        if "SEND" in x:
            headers = {'Content-Type':'application/json'}
            r = requests.post(os.getenv('ENDPOINT'), headers=headers, data=json.dumps(payload))
