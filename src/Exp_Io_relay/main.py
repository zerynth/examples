###############################################################################
# EXP-IO: Relay library example over a DC circuit (60 Vdc max)
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

# Initialize board
board.init()
# Pass the rotative switch selector position
# address = 0x11, interrupt = INTR
io_sw_sel = (1, 0,)
# Add the EXP-IO to the board
# All pin of the EXP-IO will be initialized correctly
exp_io = board.next_expansion(io, io_sw_sel)
out1 = exp_io.OUT1
# Use gpio api to control EXP-IO Outputs
while True:
    print("Toggling output 1")
    # Switch output 1
    if exp_io.is_out_on(out1):
        exp_io.out_off(out1)
    else:
        exp_io.out_on(out1)
    # sleep 1 second
    sleep(1000)
