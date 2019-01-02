from helpers import *
import sched, time
s = sched.scheduler(time.time, time.sleep)

def get_data(sc):
    temp = get_temp()
    press = get_press()
    alt = get_alt(1013.25, press, temp)
    to_send("t", temp)
    to_send("p", press)
    to_send("a", alt)
    s.enter(0.2, 1, get_data, (sc,))

s.enter(0.2, 1, get_data, (s,))
s.run()