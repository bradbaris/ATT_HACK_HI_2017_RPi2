#!/usr/bin/env python

# http://raspberrypi.stackexchange.com/q/51498
import os
import json
import time
import serial
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

busapi = requests.get("http://api.thebus.org/arrivals/", params=[('key', os.getenv('BUSHEA')),('stop', str(randint(12,20)))])
root = ET.fromstring(busapi.text)
headsign = root[2][3].text
direction = root[2][5].text
name = "User"
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
            payload = {"channel": "#doorbell-test", "username": "RailFare", "text": name+" purchased rail fare at '"+headsign+"' station at "+time, "icon_emoji": ":monorail:"}
        if(choice == 2):
            payload = {"channel": "#doorbell-test", "username": "TheBusFare", "text": name+" purchased bus fare at '"+headsign+"' ("+direction+") at "+time, "icon_emoji": ":oncoming_bus:"}
        if(choice == 3):
            payload = {"channel": "#doorbell-test", "username": "Bikeshare", "text": name+" purchased a bikeshare ride at '"+headsign+"' at "+time, "icon_emoji": ":bikeshare:"}
        if "SEND" in x:
            headers = {'Content-Type':'application/json'}
            r = requests.post(os.getenv('ENDPOINT'), headers=headers, data=json.dumps(payload))
