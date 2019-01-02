# Functions
## get_temp()
Function to get the current temperature from the connected sensor

## get_press()
Function to get the current pressure from the connected sensor

## get_alt(P0, P, T)
Function to get the current altitude from the given data.
P0 = pressure on the ground
P = current pressure
T = current temperature

## to_send(topic, value)
Function to send the data to the ground, also saves the data to a file in the data folder.
topic = what value is send
value = the data that connects to the value