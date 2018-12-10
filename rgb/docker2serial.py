#!/usr/bin/env python3

from functools import reduce

import serial
import time
import random
import docker

ser = serial.Serial('/dev/arduino')
ser.baudrate = 9600

d = docker.from_env()
w = b''    

while True:
    conts = map(lambda c: str(c.image), d.containers.list())
    conts = reduce(lambda a, b: a + b, conts, "")
    
    print(conts)
    
    r = "/red_lantern" in conts
    g = "/green_lantern" in conts
    b = "/blue_lantern" in conts
    print(r)
    print(g)
    print(b)
       
    if r & g & b:
        w = b'w'
    elif r & b:
        w = b'm'
    elif r & g:
        w = b'y'
    elif g & b:
        w = b'c'
    elif r:
        w = b'r'
    elif g:
        w = b'g'
    elif b:
        w = b'b'
    else:
        w = b'k'
    
    ser.write(w)
    time.sleep(.5)
