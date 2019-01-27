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
    s.enter(0.2, 1, get_data, (sc,))

s.enter(0.2, 1, get_data, (s,))
s.run()