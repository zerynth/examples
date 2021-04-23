###############################################################################
# EXP-IO: Interrupt
###############################################################################

# First, import the board module from the bsp (board support package).
# The bsp loads board specific names, variables and settings so that
# this project can be run on different Zerynth hardware
# without changing a line of code.
from bsp import board

import gpio

# Rising edge callback function
def rise_function():
    print("Positive edge triggered")

# Falling edge callback function
def fall_function():
    print("Negative edge triggered")

# Initialize pins as INPUT
gpio.mode(D35, INPUT_PULLDOWN)
gpio.mode(D36, INPUT_PULLUP)
# Set the callbacks to the two Pins
gpio.on_rise(D35, rise_function)
gpio.on_fall(D34, fall_function)

while True:
    # Get the current value of the DIN1
    print("D35 =", gpio.get(D35))
    # Get the current value of the DIN2
    print("D36 =", gpio.get(D36))
    # Sleep 3 seconds
    sleep(3000)
