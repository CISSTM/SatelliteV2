"""
This are the helperfunction for the main programme
"""
from os import path

import json
import datetime

from calc import get_altitude

import board
import busio
import serial

import temperature_driver
import gyro_driver



BASEPATH = path.dirname(__file__)
I2C = busio.I2C(board.SCL, board.SDA)
try:
    BME280 = temperature_driver.Adafruit_BME280_I2C(I2C)
except RuntimeError:
    print("BMP280 not connected")
except Exception:
    print("Unknown error")

try:
    BNO055 = gyro_driver.BNO055(I2C)
except RuntimeError:
    print("BNO055 not connected")
except Exception:
    print("Unkown error")

TIMES_SEND = 0
TIMES_SAVED = 0
CURRENT_FILE_OUTPUT = []

try:
    SER = serial.Serial('/dev/ttyS0', 9600, timeout=1)
except Exception:
    print("Cannot make serial connection")
def get_temp():
    """
    The function that gets the temperature
    """
    try:
        temp = BME280.temperature
        return temp
    except RuntimeError:
        print("BMP280 not connected")
        temp = get_backup_temp()
        return temp
    except Exception as error:
        print(error)
        return 9999

def get_backup_temp():
    """
    This is the function for if the BMP280 malfunctions
    """
    try:
        temp = BNO055.temperature
        return temp
    except RuntimeError:
        print("BNO055 not connected")
        return 2222
    except Exception:
        return 9999

def get_press():
    """
    The function that gets the pressure
    """
    try:
        press = BME280.pressure
        return press
    except RuntimeError:
        print("BMP280 not connected")
        return 1111
    except Exception:
        return 9999

def get_acc():
    """
    The function that gets the acceleration
    """
    try:
        acc = BNO055.linear_acceleration[2]
        return acc
    except RuntimeError:
        print("BNO055 not connected")
        return 2222
    except Exception:
        return 9999

def get_x_angle():
    """
    The function that gets the x angle
    """
    try:
        angle = BNO055.euler[0]
        return angle
    except RuntimeError:
        print("BNO055 not connected")
        return 2222
    except Exception:
        return 9999

def get_y_angle():
    """
    The function that gets the y angle
    """
    try:
        angle = BNO055.euler[1]
        return angle
    except RuntimeError:
        print("BNO055 not connected")
        return 2222
    except Exception:
        return 9999

def get_z_angle():
    """
    The function that gets the z angle
    """
    try:
        angle = BNO055.euler[2]
        return angle
    except RuntimeError:
        print("BNO055 not connected")
        return 2222
    except Exception:
        return 9999

def get_mag_x():
    """
    The function that gets the x mag
    """
    try:
        mag = BNO055.magnetometer[0]
        return mag
    except RuntimeError:
        print("BNO055 not connected")
        return 2222
    except Exception:
        return 9999

def get_mag_y():
    """
    The function that gets the y mag
    """
    try:
        mag = BNO055.magnetometer[1]
        return mag
    except RuntimeError:
        print("BNO055 not connected")
        return 2222
    except Exception:
        return 9999

def get_gravity():
    """
    The function that gets the gravity
    """
    try:
        gravity = BNO055.gravity[2]
        return gravity
    except RuntimeError:
        print("BNO055 not connected")
        return 2222
    except Exception:
        return 9999

def get_alt(pressure_0, pressure_now, temperature_now):
    """
    The function that calculates the altitude
    """
    try:
        return get_altitude(temperature_now, pressure_now, pressure_0)
    except Exception:
        return 9999

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

    try:
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
    except Exception:
        print("Error converting to short string")
        str_to_send = "1111111122"

    ## Add to current save
    CURRENT_FILE_OUTPUT.append(total)

    if TIMES_SEND % 100 == 0:
        try:
            with open(BASEPATH + '/../data/data' + str(datetime.datetime.now().year) + \
                '-' + str(datetime.datetime.now().month) + \
                '-' + str(datetime.datetime.now().day) + \
                '-' + str(datetime.datetime.now().hour) + \
                ',' + str(datetime.datetime.now().minute) + \
                ',' + str(datetime.datetime.now().second) + '.json', 'w+') as file_backup:
                json.dump(CURRENT_FILE_OUTPUT, file_backup)
                CURRENT_FILE_OUTPUT = []
            TIMES_SAVED += 1
        except Exception:
            print("Cannot save, so just sending for now.")
            CURRENT_FILE_OUTPUT = []
    try:
        sending = int(str_to_send)
        byte_send = sending.to_bytes(4, byteorder='big')
        SER.write(byte_send)
    except Exception:
        print("Cannot send, just saving for now")
    print(total)
