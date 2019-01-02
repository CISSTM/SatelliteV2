from collections import OrderedDict
from os import path
import json
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
    ##There needs to be a function that sends the data
    #print (int(str(output), 10))    
    print (output)
    return

