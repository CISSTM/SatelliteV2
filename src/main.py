"""
This is the main part, it makes the calls from the helpers file
"""

import sched
import time

from helpers import get_temp, get_press, get_alt, get_acc, get_angles, \
     get_magnets, get_gravity, get_distance, to_send

SCHEDULE = sched.scheduler(time.time, time.sleep)

FIRST_PRESS = get_press()
if FIRST_PRESS in (1111, 9999):
    FIRST_PRESS = 1013.25

def get_data(schedule_call):
    """
    The function that just makes sure everything gets called
    """
    temp = get_temp()
    press = get_press()
    alt = get_alt(FIRST_PRESS, press, temp)
    to_send("temperature", temp)
    to_send("pressure", press)
    to_send("altitude", alt)
    to_send("baccelleration", get_acc())
    angles = get_angles()
    to_send("x_angle", angles[0])
    to_send("y_angle", angles[1])
    to_send("z_angle", angles[2])
    magnets = get_magnets()
    to_send("ux_mag", magnets[0])
    to_send("vy_mag", magnets[1])
    to_send("gravity", get_gravity())
    distance, rssi = get_distance()
    to_send("distance", distance)
    to_send("rssi", rssi)
    SCHEDULE.enter(0.2, 1, get_data, (schedule_call,))

SCHEDULE.enter(0.2, 1, get_data, (SCHEDULE,))
SCHEDULE.run()
