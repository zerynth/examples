###############################################################################
# Modbus Serial Interface
################################################################################

from bsp import board
import serial
from protocols.modbus import modbus as modbus
import watchdog

# Set Watchdog timeout
watchdog.setup(10000)

def Write_One_Register(master, register, values=None, num=None):
    if (values == None and num == None):
        raise ValueError
    if (values != None):
        num = 0
        for i in range(len(values)):
            num += values[i] << i
    if (num > 0xffff):
        raise ValueError
    result = master.write_register(register, num)
    print("Value", result, "successfully written in the register", register)
    return result

def Read_One_Register(master, register):
    num = master.read_holding(register, 1)[0]
    out = []
    for i in range(10):
        out.append(num>>i & 1)
    return out
    
try:
    ser_e = board.get_serial_rs485()
    master_in = modbus.ModbusSerial(1, ser_e)

    print("start exchange messages")
    
    # write list of bits on register with address 2 (change it if needed)

    try:
        result = Write_One_Register(master_in, 2, values=[1, 0, 1, 0, 0, 0, 0, 0, 0, 0]) # max number of values is 16 elements  -> register 16 bit
        # read register 2 and check the resultwith
        result = Read_One_Register(master_in, 2)
        print("Get holding register 2: ", result)
    except Exception as e:
        print(e)
        
    try:
        # write single num value on register with address 3 (change it if needed)
        result = Write_One_Register(master_in, 3, num=3)
        # read register 3 and check the result
        result = Read_One_Register(master_in, 3)
        print("Get holding register 3: ", result)
    except Exception as e:
        print(e)

    watchdog.kick()    
    master_in.close()
    
except Exception as e:
    print("Exception ", e)
    master_in.close()