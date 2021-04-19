###############################################################################
# EXP-SER
###############################################################################

# Welcome to EXP-SER example.
# Let's see how to initialize and use the EXP-RELAY with RS485
# Zerynth will handle the RTS pin of the RS485 by its own.

# First, import the board module from the bsp (board support package).
# The bsp loads board specific names, variables and settings so that
# this project can be run on different Zerynth hardware
# without changing a line of code.
from bsp import board

from expansions import ser
import serial

# Initialize ZM1-DB
board.init()
# Pass te rotative switch selector position
# Interrupt pin INTR
ser_sw_sel = (0,)
# Add the EXP-SER to the ZM1-DB
# All pin of the EXP-SER will be initialized correctly
exp_ser = board.next_expansion(ser, ser_sw_sel)
# Initialize RS485 protocol on the serial1 and get class
ser_rs485 = exp_ser.get_serial(mode=serial.MODE_RS485_HALF_DUPLEX)

while True:
    # Write a message on the rs485 peripheral
    ser_rs485.write("Hello EXP-SER!\n")
    # sleep 1 second
    sleep(1000)
