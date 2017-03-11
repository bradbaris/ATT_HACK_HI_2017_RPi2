#!/usr/bin/env python

# http://raspberrypi.stackexchange.com/q/51498
import os
import json
import time
import serial     
import requests
from random import randint

ser = serial.Serial(
    port='/dev/ttyACM0',
    baudrate = 115200,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
    bytesize=serial.EIGHTBITS,
    timeout=1
)

name = "User"
while 1:
    x=ser.readline()
    if(x != ''):
        print(x)
        if "NAME=" in x:
            name = x[5:-1]
        num = randint(1,4)
        if(num == 1):
            payload = {"channel": "#doorbell-test", "username": "RailFare", "text": name+" purchased rail fare at Halekauwila station at 5:00PM", "icon_emoji": ":monorail:"}
        if(num == 2):
            payload = {"channel": "#doorbell-test", "username": "TheBusFare", "text": name+" purchased bus fare at Ala Moana station at 12:30PM", "icon_emoji": ":oncoming_bus:"}
        if(num == 3):
            payload = {"channel": "#doorbell-test", "username": "Bikeshare", "text": name+" purchased a bikeshare ride at Diamond Head station at 8:00AM", "icon_emoji": ":bikeshare:"}
        if "SEND" in x:
            headers = {'Content-Type':'application/json'}
            r = requests.post(os.getenv('ENDPOINT'), headers=headers, data=json.dumps(payload))
