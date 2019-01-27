from helpers import *
import sched, time
s = sched.scheduler(time.time, time.sleep)
first_press = get_press()

def get_data(sc):
    temp = get_temp()
    press = get_press()
    alt = get_alt(first_press, press, temp)
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
    s.enter(0.2, 1, get_data, (sc,))

s.enter(0.2, 1, get_data, (s,))
s.run()