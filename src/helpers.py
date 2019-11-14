"""
These are the helper functions for the main program
"""
from os import path

import json
import datetime
import logging

from calc import get_altitude, get_distance_rssi

import board
import busio
import serial

import adafruit_rfm69
import temperature_driver
import gyro_driver

FILE_LOGGER = logging.FileHandler('log.txt')
FILE_LOGGER.setLevel(logging.WARNING)
FILE_LOGGER.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - %(message)s"))

CONSOLE_LOGGER = logging.StreamHandler()
CONSOLE_LOGGER.setLevel(logging.info)
CONSOLE_LOGGER.setFormatter(logging.Formatter("%(message)s (%(levelname)s)"))

BASEPATH = path.dirname(__file__)
I2C = busio.I2C(board.SCL, board.SDA)
FREQ = 868.0

try:
    BME280 = temperature_driver.Adafruit_BME280_I2C(I2C)
    logging.debug("Connected to BME280")
except RuntimeError:
    logging.error("BMP280 not connected")
except Exception as error:
    logging.error(error)

try:
    BNO055 = gyro_driver.BNO055(I2C)
    logging.debug("Connected to BNO055")
except RuntimeError:
    logging.error("BNO055 not connected")
except Exception as error:
    logging.error(error)

try:
    SPI = busio.SPI(board.SCK, MOSI=board.MOSI, MISO=board.MISO)
    CS = board.CE0
    RESET = board.D5
    RFM69 = adafruit_rfm69.RFM69(SPI, CS, RESET, FREQ)
    logging.debug("Connected to RFM69")
except RuntimeError:
    logging.error("Cannot connect to RFM69")
except Exception as error:
    logging.error(error)

TIMES_SEND = 0
TIMES_SAVED = 0
CURRENT_FILE_OUTPUT = []

try:
    SER = serial.Serial('/dev/ttyS0', 9600, timeout=1)
    logging.debug("Connected to 433MHz transmitter")
except Exception:
    print("Cannot make serial connection")

def get_temp():
    """
    The function that gets the temperature
    """
    try:
        temp = BME280.temperature
        logging.debug("Got temperature")
        return temp
    except RuntimeError:
        logging.error("BMP280 not connected")
        temp = get_backup_temp()
        return temp
    except Exception as error:
        logging.error(error)
        return 9999

def get_backup_temp():
    """
    This is the function for if the BMP280 malfunctions
    """
    try:
        temp = BNO055.temperature
        logging.warning("Got backup temperature")
        return temp
    except RuntimeError:
        logging.error("BNO055 not connected")
        return get_backup_temp_2()
    except Exception as error:
        logging.error(error)
        return 9999

def get_backup_temp_2():
    """
    This is the third way to get the temperature
    """
    try:
        temp = RFM69.temperature
        logging.warning("Got second backup temperature")
        return temp
    except RuntimeError:
        logging.error("RFM69 not connected")
        return 2222
    except Exception as error:
        logging.error(error)
        return 9999

def get_press():
    """
    The function that gets the pressure
    """
    try:
        press = BME280.pressure
        logging.debug("Got pressure")
        return press
    except RuntimeError:
        logging.error("BMP280 not connected")
        return 1111
    except Exception as error:
        logging.error(error)
        return 9999

def get_acc():
    """
    The function that gets the acceleration
    """
    try:
        acc = BNO055.linear_acceleration[2]
        logging.debug("Got acceleration")
        return acc
    except RuntimeError:
        logging.error("BNO055 not connected")
        return 2222
    except Exception as error:
        logging.error(error)
        return 9999

def get_angles():
    """
    The function that gets angles
    """
    try:
        data = BNO055.euler
        angle = (data[0], data[1], data[2])
        logging.debug("Got angles")
        return angle
    except RuntimeError:
        logging.error("BNO055 not connected")
        return (2222, 2222, 2222)
    except Exception as error:
        logging.error(error)
        return 9999

def get_magnets():
    """
    The function that gets the magnets
    """
    try:
        data = BNO055.magnetometer
        mag = (data[0], data[1])
        logging.debug("Got magnet data")
        return mag
    except RuntimeError:
        logging.error("BNO055 not connected")
        return (2222, 2222)
    except Exception as error:
        logging.error(error)
        return (9999, 9999)

def get_gravity():
    """
    The function that gets the gravity
    """
    try:
        gravity = BNO055.gravity[2]
        logging.debug("Got gravity")
        return gravity
    except RuntimeError:
        logging.error("BNO055 not connected")
        return 2222
    except Exception as error:
        logging.error(error)
        return 9999

def get_alt(pressure_0, pressure_now, temperature_now):
    """
    The function that calculates the altitude
    """
    try:
        altitude = get_altitude(temperature_now, pressure_now, pressure_0)
        logging.debug("Calculated altitude")
        return altitude
    except Exception as error:
        logging.warning(error)
        return 9999

def get_distance():
    """
    Calculate the distance to object
    """
    try:
        rssi = RFM69.rssi
        logging.debug("Got RSSI data")
        distance = get_distance_rssi(rssi, FREQ, 2.2, 1)
        logging.debug("Calculated distance")
        return distance
    except RuntimeError:
        logging.error("RFM69 not connected")
    except Exception as error:
        logging.error(error)


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
        logging.debug("Converted float to int")
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
            logging.debug("Negative value converted to positive int")
        while value > 9999:
            value = value/10
            value = int(value)
            logging.debug("Value to big, dividing by 10")
        ## Add the value
        str_to_send += str(format(value, '04d'))
        ## Add closing message
        str_to_send += "22"
    except Exception:
        logging.error("Error converting to short string")
        str_to_send = "1111111122"

    ## Add to current save
    CURRENT_FILE_OUTPUT.append(total)
    logging.debug("Added data to data array")

    if TIMES_SEND % 100 == 0:
        try:
            with open(BASEPATH + '/../data/data' + str(datetime.datetime.now().year) + \
                '-' + str(datetime.datetime.now().month) + \
                '-' + str(datetime.datetime.now().day) + \
                '-' + str(datetime.datetime.now().hour) + \
                ',' + str(datetime.datetime.now().minute) + \
                ',' + str(datetime.datetime.now().second) + '.json', 'w+') as file_backup:
                logging.debug("Created file to save data")
                json.dump(CURRENT_FILE_OUTPUT, file_backup)
                logging.debug("Saved data to file")
                CURRENT_FILE_OUTPUT = []
                logging.debug("Cleared data array")
            TIMES_SAVED += 1
        except Exception:
            logging.warning("Cannot save, so just sending for now.")
            CURRENT_FILE_OUTPUT = []
    try:
        sending = int(str_to_send)
        logging.debug("Convert data to int for smaller packet size")
        byte_send = sending.to_bytes(4, byteorder='big')
        logging.debug("Convert int to bytes, trying to send bytes")
        SER.write(byte_send)
        logging.debug("Send data with 433MHz transmitter")
    except Exception:
        logging.warning("Cannot send, just saving for now")
    logging.info(total)
