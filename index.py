#!/usr/bin/env python

# http://raspberrypi.stackexchange.com/q/51498
import time
import serial     
import requests

url = 'https://hooks.slack.com/services/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'
payload = {"channel": "#general", "username": "webhookbot", "text": "This is posted to #general and comes from a bot named webhookbot.", "icon_emoji": ":ghost:"}

ser = serial.Serial(
    port='/dev/ttyACM0',
    baudrate = 115200,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
    bytesize=serial.EIGHTBITS,
    timeout=1
)
counter=0
while 1:
    x=ser.readline()
    if(x != ''):
        print(x)
        if "SEND" in x: 
            r = requests.post(url, data=payload)
