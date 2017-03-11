#!/usr/bin/env python
import time
import serial     
from subprocess import call

ser = serial.Serial(
    port='/dev/ttyACM0',
    baudrate = 115200,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
    bytesize=serial.EIGHTBITS,
    timeout=1
)
counter=0
call(["./spa", "args", "to", "spa"])
while counter<10:
    counter += 1
while 1:
    x=ser.readline()
    if(x != ''):
        print(x)