###############################################################################
# EXP-IO: Interrupt on opto-isolated
###############################################################################

# First, import the board module from the bsp (board support package).
# The bsp loads board specific names, variables and settings so that
# this project can be run on different Zerynth hardware
# without changing a line of code.
from bsp import board
from expansions import io
import gpio

# Rising edge callback function
def rise_function():
    print("Positive edge triggered")

# Falling edge callback function
def fall_function():
    print("Negative edge triggered")

# Initialize board
board.init()

# Pass the rotative switch selector position
# address = 0x11, interrupt = INTR
io_sw_sel = (1, 0,)

# Add the EXP-IO to the board
# All pin of the EXP-IO will be initialized correctly
exp_io = board.next_expansion(io, io_sw_sel)

# Set the callbacks to the two EXP-IO DIN
gpio.on_rise(exp_io.DIN1, rise_function)
gpio.on_fall(exp_io.DIN2, fall_function)

while True:
    # Get the current value of the DIN1
    print("DIN1 =", exp_io.din_get(exp_io.DIN1))
    # Get the current value of the DIN2
    print("DIN2 =", exp_io.din_get(exp_io.DIN2))
    # Sleep 3 seconds
    sleep(3000)
