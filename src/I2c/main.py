#######################################################
# I2c
########################################################


# First, import the board module from the bsp (board support package).
# The bsp loads board specific names, variables and settings so that
# this project can be run on different Zerynth hardware
# without changing a line of code.
from bsp import board

import i2c

'''
This i2c test works with db zm1 writing on 
output register of pcal65424
'''

sleep(2000)

i2c_scan_buf = i2c.scan(n_scan=100)

for addr in i2c_scan_buf:
    print("addr", addr, "present")

i2c_dev = i2c.I2c(32) # 0x20
write_buf = [4, 0]
read_cmd = [4]
write_buf = bytearray(write_buf)
read_cmd = bytearray(read_cmd)

for i in range(0, 8):
    write_buf[1] = i
    i2c_dev.write(write_buf)
    sleep(100)
    rx = i2c_dev.write_read(read_cmd, 1)
    print("read:", rx[0])

while True:
    sleep(100)
