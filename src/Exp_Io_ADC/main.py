###############################################################################
# EXP-IO: ADC channel example over an industrial temperature sensor
###############################################################################

from expansions import io
from bsp import board
from zsensors import sensor
import watchdog
import threading as th
import gpio
import adc
import mcu

# Initialize board
board.init()

# Pass the rotative switch selector position
# address = 0x11, interrupt = INTR
io_sw_sel = (1, 0,)

# Add the EXP-IO to the board
# All pin of the EXP-IO will be initialized correctly
exp_io = board.next_expansion(io, io_sw_sel)

# Lock for sync
core_sample_lock = th.Lock()
ready = True

# Set Watchdog timeout
watchdog.setup(60000)

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
            temp = exp_io.read_resistive(1)
            print(" - temp    :", temp)        
            print("======== done")
        except Exception as e:
            print("Generic Error:", e)
            board.error_cloud()
            mcu.reset()
    
try:
    print("adc config...")
    #Create a dictionary with all sensors
    d = sensor.get_sensors_dict()
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
