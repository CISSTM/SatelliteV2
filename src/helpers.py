import math
import json
import argparse
import logging

import board
import digitalio
import busio
import time
import temperature_driver
from collections import OrderedDict
from os import path

basepath = path.dirname(__file__)
i2c = busio.I2C(board.SCL, board.SDA)
bme280 = temperature_driver.Adafruit_BME280_I2C(i2c)


times_send =  0
times_saved = 0
current_file_output = []

def get_temp():
    temp = bme280.temperature
    return temp

def get_press():
    press = bme280.pressure
    return press

def get_alt(P0, P, T):
    h = (((P0/P)**(1/5.257)-1)*(T+273.15))/(0.0065)
    return h;

def to_send(topic, value):
    global times_send
    global times_saved
    global current_file_output
    times_send += 1

    # Round numbers for when to send
    if isinstance(value, float):
        value = int(value)
    
    total = {
        topic: value,
        "s": times_send
    }

    ## Starting message
    str_to_send = "11"
    ## Topic number
    str_to_send += str(ord(topic[0])-31)
    ## Add the value
    str_to_send += str(format(value, '04d'))
    ## Add closing message
    str_to_send += "22"

    ## Add to current save
    current_file_output.append(total)

    ## If it has send a 100 times save the file
    if (times_send % 100 == 0):
        ## Open or create file to save to
        with open(basepath + '/../data/data' + str(times_saved) +'.json', 'w+') as file_backup:
            ##Save to a file
            json.dump(current_file_output, file_backup)
            ## Clear to save
            current_file_output = []
        ## +1 for time saved so that it saves to a new file
        times_saved += 1
    
    ## Convert the string to int to send
    to_send = int(str_to_send)
    print (total)
    return

def send(code):
    print ("no way to send yet")