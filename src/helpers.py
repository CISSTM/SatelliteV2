"""
This are the helperfunction for the main programme
"""
from os import path


import json
import datetime

import board
import busio
import serial
import temperature_driver
import gyro_driver


BASEPATH = path.dirname(__file__)
I2C = busio.I2C(board.SCL, board.SDA)
BME280 = temperature_driver.Adafruit_BME280_I2C(I2C)
BNO055 = gyro_driver.BNO055(I2C)

TIMES_SEND = 0
TIMES_SAVED = 0
CURRENT_FILE_OUTPUT = []

SER = serial.Serial('/dev/ttyS0', 9600, timeout=1)

def get_temp():
    """
    The function that gets the temperature
    """
    temp = BME280.temperature
    return temp

def get_press():
    """
    The function that gets the pressure
    """
    press = BME280.pressure
    return press

def get_acc():
    """
    The function that gets the acceleration
    """
    acc = BNO055.linear_acceleration[2]
    return acc

def get_x_angle():
    """
    The function that gets the x angle
    """
    angle = BNO055.euler[0]
    return angle

def get_y_angle():
    """
    The function that gets the y angle
    """
    angle = BNO055.euler[1]
    return angle

def get_z_angle():
    """
    The function that gets the z angle
    """
    angle = BNO055.euler[2]
    return angle

def get_mag_x():
    """
    The function that gets the x mag
    """
    mag = BNO055.magnetometer[0]
    return mag

def get_mag_y():
    """
    The function that gets the y mag
    """
    mag = BNO055.magnetometer[1]
    return mag

def get_gravity():
    """
    The function that gets the gravity
    """
    gravity = BNO055.gravity[2]
    return gravity

def get_alt(pressure_0, pressure_now, temperature_now):
    """
    The function that calculates the altitude
    """
    height = (((pressure_0/pressure_now)**(1/5.257)-1)*(temperature_now+273.15))/(0.0065)
    if height < 0:
        height = abs(height) + 9000
    return height

def to_send(topic, value):
    """
    The function that sends and saves
    """
    global TIMES_SEND
    global TIMES_SAVED
    global CURRENT_FILE_OUTPUT
    TIMES_SEND += 1

    # Round numbers for when to send
    if isinstance(value, float):
        value = int(value)
    total = {
        topic: value,
        "s": TIMES_SEND
    }

    ## Starting message
    str_to_send = "11"
    ## Topic number
    str_to_send += str(ord(topic[0])-31)
    if value < 0:
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
    CURRENT_FILE_OUTPUT.append(total)

    if TIMES_SEND % 100 == 0:
        with open(BASEPATH + '/../data/data' + str(datetime.datetime.now().year) + '-'+ \
            str(datetime.datetime.now().month) + '-' + str(datetime.datetime.now().day) + \
            '-' + str(datetime.datetime.now().hour) + ',' + str(datetime.datetime.now().minute) + \
            ',' + str(datetime.datetime.now().second) + '.json', 'w+') as file_backup:
            json.dump(CURRENT_FILE_OUTPUT, file_backup)
            CURRENT_FILE_OUTPUT = []
        TIMES_SAVED += 1
    sending = int(str_to_send)
    byte_send = sending.to_bytes(4, byteorder='big')
    SER.write(byte_send)
    print(total)
    return
