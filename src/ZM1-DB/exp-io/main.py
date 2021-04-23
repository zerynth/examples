###############################################################################
# EXP-IO
###############################################################################

# Welcome to EXP-IO example.
# Let's see how to initialize and use outputs and inputs
# both digital and analog of the EXP-IO.

# First, import the board module from the bsp (board support package).
# The bsp loads board specific names, variables and settings so that
# this project can be run on different Zerynth hardware
# without changing a line of code.
from bsp import board

from expansions import io
import gpio
import adc

# Initialize ZM1-DB
board.init()
# Pass te rotative switch selector position
# address = 0x11, interrupt = INTR
io_sw_sel = (1, 0,)
# Add the EXP-IO to the ZM1-DB
# All pin of the EXP-IO will be initialized correctly
exp_io = board.next_expansion(io, io_sw_sel)

# Use gpio api to control EXP-IO Outputs and Inputs
gpio.high(exp_io.OUT1)
while True:
    # Switch output 1 logic value
    gpio.toggle(exp_io.OUT1)
    # Read and print digital input 1 value
    print("DIN1 =", gpio.get(exp_io.DIN1))
    # Read and print analog input 1 value (1 sample)
    print("AIN1 =", adc.read(exp_io.AIN1, 1))
    # sleep 1 second
    sleep(1000)
