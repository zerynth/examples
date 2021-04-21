###############################################################################
# EXP-IO: ADC channel example over an industrial temperature sensor
###############################################################################

# First, import the board module from the bsp (board support package).
# The bsp loads board specific names, variables and settings so that
# this project can be run on different Zerynth hardware
# without changing a line of code.
from bsp import board

from expansions import io
from zsensors import sensor

# Initialize board
board.init()

# Pass the rotative switch selector position
# address = 0x11, interrupt = INTR
io_sw_sel = (1, 0,)

# Add the EXP-IO to the board
# All pin of the EXP-IO will be initialized correctly
exp_io = board.next_expansion(io, io_sw_sel)

# Create a dictionary with all sensors
# Sensors can be accesses using the key passed on the
# json configuration file ("temperature" in this case)
sens_dict = sensor.get_sensors_dict()
print("Created sensor class")

while True:
    # Read and print the current temperature read by the sensor
    print("temperature:", sens_dict["temperature"].read())
    sleep(1000)
