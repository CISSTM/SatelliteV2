from helpers import *
import sys
print("Current python version: "+str(sys.version_info))

get_alt(1013.25, get_press(), get_temp())

for i in range (0, 200):
    to_send("s", 200)
