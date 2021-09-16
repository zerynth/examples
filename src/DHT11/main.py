################################################################################
# DHT11 Sensor
################################################################################

# This example shows how to configure and use the DHT11 sensor to read temperature
# and humidity.

# First, import the board module from the bsp (board support package).
# The bsp loads board specific names, variables and settings so that
# this project can be run on different Zerynth hardware
# without changing a line of code.

from bsm import board
from components.dht11 import dht11

while True:
    # sleep 1 second
    sleep(1000)
    try:
        # Read temperature and humidity from DHT11
        print(dht11.read(D32))
    except Exception as e:
        print(e)