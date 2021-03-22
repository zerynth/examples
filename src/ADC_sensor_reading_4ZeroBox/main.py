################################################################################
# 4ZeroBox Sensor Reading
################################################################################

import mcu
import threading as th
import watchdog
from bsp import board

# Lock for sync
core_sample_lock = th.Lock()
ready = True
# Set Watchdog timeout
watchdog.setup(60000)
# Init sys
print('init')

# Reference table for no linear NTC sensor
ref_table = [329.5,247.7,188.5,144.1,111.3,86.43,67.77,53.41,42.47,33.90,27.28,22.05,17.96,14.69,12.09,10.00,8.313,
              6.940,5.827,4.911,4.160,3.536,3.020,2.588,2.228,1.924,1.668,1.451,1.266,1.108,0.9731,0.8572,0.7576]

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
            analog_val = board.read_420(1)
            temp_1 = board.read_resistive(1)
            temp_2 = board.read_resistive(2)
            temp_3 = board.read_resistive(3)
            power = board.read_power(1)
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
    # Config FourZeroBox ADC channels: config_adc(label, ch, pga, sps)
    board.config_adc(board.ADC_010_420, 1, 2, 7)
    board.config_adc(board.ADC_RES, 1, 2, 7)
    board.config_adc(board.ADC_RES, 2, 2, 7)
    board.config_adc(board.ADC_RES, 3, 2, 7)
    board.config_adc(board.ADC_CUR, 1, 2, 7)
    # Config FourZeroBox ADC conversion parameters
    board.set_conversion_010_420(1, 0, 100, 0, 0, 100)      # (ch, y_min, y_max, offset=0, under_x=None, over_x=None)
    board.set_conversion_resistive(1, -50, ref_table, 5)    # (ch, v_min, ref_table, delta, offset=0)
    board.set_conversion_resistive(2, -50, ref_table, 5)
    board.set_conversion_resistive(3, -50, ref_table, 5)
    board.set_conversion_current(1, 1, 3000, 230, 0)        # (ch, n_samples=400, ncoil=1, ratio=2000, voltage=220, offset=0)
    print("adc config done")
except Exception as e:
    print(e)
    mcu.reset()

try:
    print("Start read_event_handler thread")
    thread(read_event_handler)
    print('start main')
    # Main Loop
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
