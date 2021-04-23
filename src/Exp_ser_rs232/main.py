###############################################################################
# EXP-SER: RS232
###############################################################################

# First, import the board module from the bsp (board support package).
# The bsp loads board specific names, variables and settings so that
# this project can be run on different Zerynth hardware
# without changing a line of code.
from bsp import board

from expansions import ser
import serial
import msg_exchange


# Initialize board
board.init()
# Pass the rotative switch selector position
# Interrupt pin INTR
ser_sw_sel = (0,)
# Add the EXP-SER to the board
# All pin of the EXP-SER will be initialized correctly
exp_ser1 = board.next_expansion(ser, ser_sw_sel)
# Initialize serial1
ser1 = exp_ser1.get_serial(ser=SERIAL1, mode=serial.MODE_UART, flow_ctrl=serial.HW_FLOWCTRL_CTS_RTS)

while True:
    # From msg_exchange call the ping_starter function on one board
    # and ping_receiver on the other to start a PING-PONG between the two.

    # Uncomment to create the PING sender
    msg_exchange.ping_starter(ser1)

    #Uncomment to create the PING receiver
    # msg_exchange.ping_receiver(ser1)