###############################################################################
# EXP-SER: ModbusSerial over RS485 with external industrial module
###############################################################################

# Welcome to EXP-SER example.
# Let's see how to initialize and use the EXP-SER with RS485
# Zerynth will handle the RTS pin of the RS485 by its own.


# First, import the board module from the bsp (board support package).
# The bsp loads board specific names, variables and settings so that
# this project can be run on different Zerynth hardware
# without changing a line of code.
from bsp import board

from expansions import ser
from protocols.modbus import modbus
import serial

# Write one register using modbus protocol.
def Write_One_Register(master, register, num):
    if (num > 0xFFFF):
        raise ValueError
    result = master.write_register(register, num)
    print("Value", result, "successfully written in the register", register)
    return result

# Read one register using modbus protocol
def Read_One_Register(master, register):
    return master.read_holding(register, 1)[0]

# Initialize board
board.init()
# Pass the rotative switch selector position
# Interrupt pin INTR
ser_sw_sel = (0,)
# Add the EXP-SER to the board
# All pin of the EXP-SER will be initialized correctly
exp_ser = board.next_expansion(ser, ser_sw_sel)
# Get an initialized RS485 serial fro EXP-SER
ser_rs485 = exp_ser.get_serial(baud=9600, mode=serial.MODE_RS485_HALF_DUPLEX)
# Init a modbus master
master_in = modbus.ModbusSerial(1, ser_rs485)

w_val = 3
r_reg = 2
try:
    # Write one register with modbus protocol
    if Write_One_Register(master_in, r_reg, w_val):
        # Check if the register has the expected vale
        r_val = Read_One_Register(master_in, r_reg)
        print("Read value:", r_val)
except Exception as e:
    print(e)

while True:
    sleep(1000)
