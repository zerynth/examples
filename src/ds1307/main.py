################################################################################
# DS1307 RTC with IIM42652
################################################################################

# This example shows how to configure and use the DS1307 RTC to keep track
# of time. Since the DS1307 I2C clock speed is capped at 400 kHz, the example
# shows how to change the I2C clock speed to work at faster speed (1 MHz) with
# Other devices and slow down to 400 kHz only when we want to get the time from
# the DS1307.

# First, import the board module from the bsp (board support package).
# The bsp loads board specific names, variables and settings so that
# this project can be run on different Zerynth hardware
# without changing a line of code.
from bsp import board
from components.ds1307 import ds1307
from components.iim42652 import iim42652
import time

def config_iim42652(dev):
    # Software reset of the iim42652
    dev.soft_reset()
    # Set up the device for I2C communication
    dev.setup()
    # Set accel and gyro config
    # Accel ODR = 2khz, full scale = 16 g
    dev.set_accel_cfg(0b0101, 0b000)
    # Power accels and gyros on low noise mode
    dev.set_pwr_cfg(3, 0, 0, 0)

def get_last_data(dev):
    print("\n<---------------------- IIM42652 Data --------------------->")
    t = dev.get_temp()
    print("temp:", t)
    ax = dev.get_accel_x()
    ay = dev.get_accel_y()
    az = dev.get_accel_z()
    print("accels: [", ax, ",", ay, ",", az, "]")
    print("<---------------------------------------------------------->\n")

def get_and_print_time(dev):
    print("\n<--------------------------- RTC -------------------------->")
    lt = rtc.localtime()
    print(lt.to_tuple()[0:6])
    print("<---------------------------------------------------------->\n")

# Initialize RTC and set time
rtc = ds1307.DS1307(0x68, I2C0, 400000)
t = time.TimeInfo()
t.tm_sec = 0
t.tm_min = 30
t.tm_hour = 14
t.tm_mday = 10
t.tm_mon = 7
t.tm_year = 2021
rtc.settime(t)
# Initialize accelerometer
iim = iim42652.IIM42652(0x69, I2C0, 1000000)
config_iim42652(iim)
while True:
    try:
        # Slow down I2C0 clock's speed and get time
        rtc.set_clock(400000)
        get_and_print_time(rtc)
        # Speed up I2C0 clock's speed and get accelerations
        iim.set_clock(1000000)
        get_last_data(iim)
        sleep(1000)
    except Exception as e:
        print(e)