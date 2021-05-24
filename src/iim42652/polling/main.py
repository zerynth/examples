###############################################################################
# IIM-42652 in polling
###############################################################################

# IIM-42652 with polling.
# Let's see how to initialize and use the IIM-42652 and get data from fifo.


# First, import the board module from the bsp (board support package).
# The bsp loads board specific names, variables and settings so that
# this project can be run on different Zerynth hardware
# without changing a line of code.
from bsp import board
from components.iim42652 import iim42652

# Get and print last read data
def get_last_data(dev):
    print("\n<---------------------- Last Data --------------------->")
    t = dev.get_temp()
    print("temp:", t)
    ax = dev.get_accel_x()
    ay = dev.get_accel_y()
    az = dev.get_accel_z()
    gx = dev.get_gyro_x()
    gy = dev.get_gyro_y()
    gz = dev.get_gyro_z()
    print("accels: [", ax, ",", ay, ",", az, "]")
    print("gyros: [", gx, ",", gy, ",", gz, "]")
    print("<------------------------------------------------------>\n")

# Get all the data from fifo, handle them and print them
def get_fifo_data(dev, n_dat):
    b = dev.get_fifo(n_dat)
    start = 0
    print("\n<--------------------- Fifo Data --------------------->")
    print("(n_bytes, header, acc_x, acc_y, acc_z, gyr_x, gyr_y, gyr_z, temp, tmst)")
    while True:
        tup = dev.handle_fifo(b[start:])
        start += tup[0]
        print(tup)
        if start >= n_dat:
            break
    print("<------------------------------------------------------>\n")

# Create a iim42652 class with i2c
iim = iim42652.IIM42652()

sleep(500)

# Software reset of the iim42652
iim.soft_reset()
# Set up the device for I2C communication
iim.setup()

# Set accel and gyro config
# Accel ODR = 2khz, full scale = 16 g
iim.set_accel_cfg(0b0101, 0b000)
# Gyro ODR = 2khz, full scale = 2000 dps
iim.set_gyro_cfg(0b1111, 0b000)
# Configure fifo to get accels and gyros data 
iim.set_fifo_cfg(True, True)
# Set fifo data decimation, only 1 put of 100 data input will go to fifo
iim.set_fifo_decimation(100)
# Set fifo in stream mode
iim.set_fifo_mode(0b01)

# Power accels and gyros on low noise mode
iim.set_pwr_cfg(3, 3, 0, 0)

fifo_ths = 800

while True:
    sleep(1000)
    get_last_data(iim)
    # Get number of bytes on the fifo
    n = iim.fifo_cnt()
    print("Current fifo count:", n)
    if n > fifo_ths:
        # Get data if there are enough on the fifo
        print("Get data!")
        get_fifo_data(iim, n)
