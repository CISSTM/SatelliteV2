import math
import json
import argparse
import logging
import datetime

import board
import digitalio
import busio
import time
import temperature_driver
import gyro_driver

import serial

from collections import OrderedDict
from os import path

basepath = path.dirname(__file__)
i2c = busio.I2C(board.SCL, board.SDA)
bme280 = temperature_driver.Adafruit_BME280_I2C(i2c)
bno055 =  gyro_driver.BNO055(i2c)

times_send =  0
times_saved = 0
current_file_output = []

ser = serial.Serial('/dev/ttyS0', 9600, timeout=1)

def get_temp():
    temp = bme280.temperature
    return temp

def get_press():
    press = bme280.pressure
    return press

def get_acc():
    acc = bno055.linear_acceleration[2]
    return acc

def get_x_angle():
    angle = bno055.euler[0]
    return angle

def get_y_angle():
    angle = bno055.euler[1]
    return angle

def get_z_angle():
    angle = bno055.euler[2]
    return angle

def get_mag_x():
    mag = bno055.magnetometer[0]
    return mag

def get_mag_y():
    mag = bno055.magnetometer[1]
    return mag

def get_gravity():
    gravity = bno055.gravity[2]
    return gravity

def get_alt(P0, P, T):
    h = (((P0/P)**(1/5.257)-1)*(T+273.15))/(0.0065)
    if (h<0):
        h = abs(h) + 9000
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
    if (value < 0):
        value = abs(value) + 9000
        value = int(value)
    while value > 9999:
        value = value/10
        value = int(value)
    ## Add the value
    str_to_send += str(format(value, '04d'))
    ## Add closing message
    str_to_send += "22"

    ## Add to current save
    current_file_output.append(total)

    ## If it has send a 100 times save the file
    if (times_send % 100 == 0):
        ## Open or create file to save to
        with open(basepath + '/../data/data' + str(datetime.datetime.now().year) + '-'+ str(datetime.datetime.now().month) + '-' + str(datetime.datetime.now().day) + '-' + str(datetime.datetime.now().hour) + ',' + str(datetime.datetime.now().minute) + ',' + str(datetime.datetime.now().second) + '.json', 'w+') as file_backup:
            ##Save to a file
            json.dump(current_file_output, file_backup)
            ## Clear to save
            current_file_output = []
        ## +1 for time saved so that it saves to a new file
        times_saved += 1
    
    ## Convert the string to int to send
    to_send = int(str_to_send)
    byte_send = to_send.to_bytes(4, byteorder='big')
    ser.write(byte_send)
    print (total)
    return

def send(code):
    print ("no way to send yet")