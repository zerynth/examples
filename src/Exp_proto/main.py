#####################################################################################
# PROTO: Connecting BME280 temperature sensor and transmitting temperature to ZDM
#####################################################################################

# First, import the board module from the bsp (board support package).
# The bsp loads board specific names, variables and settings so that
# this project can be run on different Zerynth hardware
# without changing a line of code.
from bsp import board

import i2c
from components.bme280 import bme280
from zsensors import sensor
from networking import wifi
from zdm import zdm
import threading as th
import watchdog
import mcu
import time

############################### INIT LOCKs/VARs/SFW ############################
# Lock for sync
core_sample_lock = th.Lock()
ready = True

# Set Watchdog timeout
watchdog.setup(60000)

################################### NETWORKING ################################
SSID = "Example-SSID"
PASSWORD = "Example-Password"

############################### THREAD DEFINITIONS ############################
def pub_event_handler():
    global ready

    while True:
        try:
            # Sync
            ready = True
            core_sample_lock.acquire()
            ready = False

            temp = sens.get_temp()
            print(" - temp[C]:      ", temp)

            print("======== SENDING TO ZDM")
            # Organize data in json dict
            to_send = {}
            to_send['temp'] = temp
            print("======== done")
            # Publish data to ZDM cloud service
            device.publish(to_send, "data")
            sleep(100)

        except Exception as e:
            print('Publish exception: ', e)
            mcu.reset()

###################################### INIT 4ZB and ZDM ######################################
try:
    # Connection to wifi network
    print("1 - Connecting to wifi ...")
    wifi.configure(SSID, PASSWORD)
    wifi.start()
    print("connected!",wifi.info())

    # Connection to ZDM
    print("2 - Connecting to ZDM ...")
    device = zdm.Agent()
    device.start()
    print("... done")
except Exception as e:
    print (e)
    mcu.reset()

try:
    print("3 - bme config...")
    sens = bme280.BME280(I2C0)
    print("... done")
except Exception as e:
    print(e)
    mcu.reset()

try:
    print("######################################")
    # Start read_event_handler thread
    print("Starting Threads")
    thread(pub_event_handler)
    print("... done")

    # Main Loop
    while True:
        sleep(1000)
        print("WiFi is online:   ", wifi.info())
        print("ZDM is online:    ", device.online())
        # Sync between main thread and pub_event_handler thread
        if ready:
            core_sample_lock.release()
            # Reset Watchdog timer
            watchdog.kick()
except Exception as e:
    print (e)
    mcu.reset()
