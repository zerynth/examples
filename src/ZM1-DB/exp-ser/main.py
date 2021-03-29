###############################################################################
# EXP-SER
###############################################################################

# Welcome to EXP-SER example.
# Let's see how to initialize and use the EXP-RELAY with RS485
# Zerynth will handle the RTS pin of the RS485 by its own.

from expansions import ser
from bsp import board
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
