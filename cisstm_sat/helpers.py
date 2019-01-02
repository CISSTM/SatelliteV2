def get_temp():
    temp = 15
    return temp

def get_press():
    press = 1000
    return press

def get_alt(P0, P, T):
    h = (((P0/P)**(1/5.257)-1)*(T+273.15))/(0.0065)
    return h;