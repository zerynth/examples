###############################################################################
# EXP-SER: RS232
###############################################################################

from expansions import ser
from bsp import board
import serial
import mcu
import watchdog
import threading as th

# Initialize board
board.init()
# Pass the rotative switch selector position
# Interrupt pin INTR
ser_sw_sel1 = (0,)
# Add the EXP-SER to the board
# All pin of the EXP-SER will be initialized correctly
exp_ser1 = board.next_expansion(ser, ser_sw_sel)
# Initialize serial1 and serial2
ser1 = exp_ser1.get_serial(ser=SERIAL1, mode=serial.MODE_UART, flow_ctrl=serial.HW_FLOWCTRL_CTS_RTS)

ser_sw_sel2 = (0,)
exp_ser2 = board.next_expansion(ser, ser_sw_sel2)
ser2 = exp_ser.get_serial(ser=SERIAL2, mode=serial.MODE_UART, flow_ctrl=serial.HW_FLOWCTRL_CTS_RTS)

# Lock for sync
core_sample_lock = th.Lock()
ready = True

# Set Watchdog timeout
watchdog.setup(60000)

# Thread function to write 
def write_handler():
    global ready

    while True:
        try:
            # Sync
            ready = True
            core_sample_lock.acquire()
            ready = False
            # Write a message
            temp = ser1.write("Hello Zerynth!")
        except Exception as e:
            print("Generic Error:", e)
            board.error_cloud()
            mcu.reset()

# Thread function to read 
def read_handler():
    global ready

    while True:
        try:
            # Sync
            ready = True
            core_sample_lock.acquire()
            ready = False
            # Read a message
            temp = ser2.read()
            print("Message: ", temp)
        except Exception as e:
            print("Generic Error:", e)
            board.error_cloud()
            mcu.reset()

try:
    print("Start threads")
    thread(write_handler())
    thread(read_handler())
    print("Start main")
    while True:
        sleep(3000)
        # Sync between main thread and pub_event_handler thread 
        if ready:
            core_sample_lock.release()
            # Reset Watchdog timer
            watchdog.kick()
except Exception as e:
    print (e)
    mcu.reset()