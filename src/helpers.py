import math
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
    rfdevice.enable_tx()
    rfdevice.tx_code(code, 1, 350, 24)
    rfdevice.cleanup()