###############################################################################
# IIM-42652 with interrupt and IIR filter
###############################################################################

# IIM-42652 with interrupt and IIR filter.
# Let's see how to initialize and use the IIM-42652 with interrupts when
# fifo is full and filter its data with an IIR filter.

# First, import the board module from the bsp (board support package).
# The bsp loads board specific names, variables and settings so that
# this project can be run on different Zerynth hardware
# without changing a line of code.
from bsp import board
from components.iim42652 import iim42652
import gpio
import threading
from filters import iir_filter

# Set to true to print all raw and filtered data
print_data = False

# Feedforward filter coefficients
b = [0.4, 0.23, 0.1, 0.09, 0.088, 0.01]
# Feedback filter coefficients
a = [0.315, 0.13, 0.07, 0.024]

# Create a filter list, one for every data input
filters = []
for i in range(6):
    filters.append(iir_filter.IIR_FILTER(b, a))

sem = threading.Semaphore(1)
sem_fil = threading.Semaphore(0)

# List that will contain raw data (xyz accelerations and xyz gyroscopes data)
xyz_datas = [[] for i in range(6)]
# List that will contain filtered data (xyz accelerations and xyz gyroscopes data)
xyz_filtered = [[] for i in range(6)]

# Prints all raw data
def print_raw_data():
    if print_data:
        d = xyz_datas
        print("\n<--------------------- Fifo Data --------------------->")
        print("( acc_x, acc_y, acc_z, gyr_x, gyr_y, gyr_z )")
        for i, dat in enumerate(d[0]):
            print("(", d[0][i], ",", d[1][i], ",", d[2][i], ",", d[3][i], ",", d[4][i], ",", d[5][i], ")")
        print("\n<----------------------------------------------------->")

# Prints all filtered data
def print_filtered_data():
    if print_data:
        d = xyz_filtered
        print("\n<------------------- Filtered Data ------------------->")
        print("( acc_x, acc_y, acc_z, gyr_x, gyr_y, gyr_z )")
        for i, dat in enumerate(d[0]):
            print("(", d[0][i], ",", d[1][i], ",", d[2][i], ",", d[3][i], ",", d[4][i], ",", d[5][i], ")")
        print("\n<----------------------------------------------------->")

# Filters all raw data and put them on the filtered data list
def filter_all():
    for i, filt in enumerate(filters):
        xyz_filtered[i] = filt.filter_array(xyz_datas[i])
        xyz_datas[i] = []

# Interrupt call back, will get fifo buffer when the fifo water-mark is reached
def get_fifo_data():
    sem.acquire()
    # Check if the int triggered from wm
    int_stat = iim.get_int_status()
    if int_stat & 0b100:
        print("Fifo wm reached!")
        # Get fifo n bytes
        n = iim.fifo_cnt()
        # Get fifo
        b = iim.get_fifo(n)
        start = 0
        while True:
            # Convert all fifo data in a tuple
            tup = iim.handle_fifo(b[start:])
            start += tup[0]
            for i, dat in enumerate(xyz_datas):
                dat.append(tup[i+2])
            if start >= n:
                break
        print_raw_data()
        # Unlock the filters
        sem_fil.release()
    sem.release()

# Create a iim42652 class with i2c
iim = iim42652.IIM42652()

sleep(500)

# Software reset of the iim42652
iim.soft_reset()
# Set up the device for I2C communication
iim.setup()

# Set accel and gyro config
# Accel ODR = 2khz, full scale = 16 g
iim.set_accel_cfg(0b1111, 0b000)
# Gyro ODR = 2khz, full scale = 2000 dps
iim.set_gyro_cfg(0b1111, 0b000)
# Configure fifo to get accels and gyros data 
iim.set_fifo_cfg(True, True, wm_gt_th=False) 
# Set fifo data decimation, only 1 put of 100 data input will go to fifo
iim.set_fifo_decimation(5)
# Set fifo in stream mode
iim.set_fifo_mode(0b01)
# Set the number of bytes on fifo to trigger interrupt
iim.set_fifo_wm(2048)

# Setup interrupt gpio on eva-board
gpio.mode(D26, INPUT_PULLUP)
gpio.on_fall(D26, get_fifo_data)
# Set iim42652 interrupt configuration:
# pin1, pulse mode, pp, active low
iim.set_int_cfg(1, 0, 1, 0)
# Set interrupt clears on fifo read
iim.set_int_clear_cfg(2, 2, 2)
# Set int sources on pin 1 as fifo full and wm reached
iim.set_int_sources(1, True, True)
# Power accels and gyros on low noise mode
iim.set_pwr_cfg(3, 3, 0, 0)

while True:
    # Wait for the fifo data to be ready
    sem_fil.acquire()
    # Filters all data
    filter_all()
    print_filtered_data()
    print("Filter done!")
