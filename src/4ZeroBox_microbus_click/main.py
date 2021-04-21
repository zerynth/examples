###############################################################################
# 4ZeroBox microbus click
################################################################################

# First, import the board module from the bsp (board support package).
# The bsp loads board specific names, variables and settings so that
# this project can be run on different Zerynth hardware
# without changing a line of code.
from bsp import board

import i2c
from components.bme280 import bme280

sens = bme280.BME280(I2C0)

while True:
    thp = sens.get_values_fast()
    print(thp)
    t = sens.get_temp()
    print("temperature: ", t)
    h = sens.get_hum()
    print("humidity: ", h)
    p = sens.get_press()
    print("pressure: ", p)
    sleep(1000)
