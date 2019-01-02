import sys
import os
sys.path.append(os.path.abspath('../src'))
import helpers

get_alt(get_press(), get_alt())

for i in range (0, 200):
    to_send("s", 200)
