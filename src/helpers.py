import sys
import json
import argparse
import logging


from collections import OrderedDict
#from rpi_rf import RFDevice
#rfdevice = RFDevice(17)
from os import path

basepath = path.dirname(__file__)


times_send =  0
times_saved = 0
current_file_output = []

def get_temp():
    temp = 15
    return temp

def get_press():
    press = 1000
    return press

def get_alt(P0, P, T):
    h = (((P0/P)**(1/5.257)-1)*(T+273.15))/(0.0065)
    return h;

def to_send(topic, value):
    global times_send
    global times_saved
    global current_file_output
    times_send += 1
    if isinstance(value, float):
        value = int(value)
    total = {
        topic: value,
        "s": times_send
    }

    current_file_output.append(total)

    if (times_send % 100 == 0):
        with open(basepath + '/../data/data' + str(times_saved) +'.json', 'w+') as file_backup:
            json.dump(current_file_output, file_backup)
            current_file_output = []
        
        times_saved += 1

    output = json.dumps(total)
    str_to_send = ""
    for i, c in enumerate(output):
        str_to_send += str(ord(c))
        str_to_send += "00"
    to_send = int(str_to_send)
    print (output)
    return

def send(code):
    rfdevice.enable_tx()
    rfdevice.tx_code(code, 1, 350, 24)
    rfdevice.cleanup()