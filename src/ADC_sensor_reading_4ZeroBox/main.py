################################################################################
# 4ZeroBox Sensor Reading
################################################################################

# First, import the board module from the bsp (board support package).
# The bsp loads board specific names, variables and settings so that
# this project can be run on different Zerynth hardware
# without changing a line of code.
from bsp import board

from zsensors import sensor
import mcu
import threading as th
import watchdog

# Lock for sync
core_sample_lock = th.Lock()
ready = True
# Set Watchdog timeout
watchdog.setup(60000)
# Init sys
board.init()
board.summary()

# Thread function for read sensor data and send them to the cloud
def read_event_handler():
    global ready

    while True:
        try:
            # Sync
            ready = True
            core_sample_lock.acquire()
            ready = False
            print("======== reading")
            # Read from 4-20mA channel1, resistive channel1/channel2/channel3, power channel1
            analog_val = sens_dict["current"].read()
            temp_1 = sens_dict["temperature_1"].read()
            temp_2 = sens_dict["temperature_2"].read()
            temp_3 = sens_dict["temperature_3"].read()
            power = sens_dict["power"].read()
            print(" - analog    :", analog_val)
            print(" - temp 1    :", temp_1)
            print(" - temp 2    :", temp_2)
            print(" - temp 3    :", temp_3)
            print(" - power     :", power)            
            print("======== done")
        except Exception as e:
            print("Generic Error:", e)
            board.error_cloud()
            mcu.reset()
    
try:
    print("adc config...")
    #Create a dictionary with all FourZeroBox sensors
    sens_dict = sensor.get_sensors_dict()
    print("adc config done")
except Exception as e:
    print(e)
    mcu.reset()

try:
    print("Start read_event_handler thread")
    thread(read_event_handler())
    print("start main")
    while True:
        sleep(1000)
        # Sync between main thread and pub_event_handler thread 
        if ready:
            core_sample_lock.release()
            # Reset Watchdog timer
            watchdog.kick()
except Exception as e:
    print (e)
    mcu.reset()
