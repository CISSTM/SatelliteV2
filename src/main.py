"""
This is the main part, it makes the calls from the helpers file
"""

import sched
import time
from helpers import get_temp, get_press, get_alt, get_acc, get_x_angle, get_y_angle, \
    get_z_angle, get_mag_x, get_mag_y, get_gravity, to_send

SCHEDULE = sched.scheduler(time.time, time.sleep)
FIRST_PRESS = get_press()

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
    to_send("x_angle", get_x_angle())
    to_send("y_angle", get_y_angle())
    to_send("z_angle", get_z_angle())
    to_send("ux_mag", get_mag_x())
    to_send("vy_mag", get_mag_y())
    to_send("gravity", get_gravity())
    SCHEDULE.enter(0.2, 1, get_data, (schedule_call,))

SCHEDULE.enter(0.2, 1, get_data, (SCHEDULE,))
SCHEDULE.run()
