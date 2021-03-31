###############################################################################
# 4ZeroBox Firmware Over The Air
###############################################################################

from bsp import board
from networking import wifi
from zdm import zdm
import threading as th
import watchdog
import mcu
import gpio

# Set the ssid and password of your wifi network
ssid = "Zerynth"
passwd = "Zerynth"

# Lock for sync
core_sample_lock = th.Lock()
ready = True
# Set Watchdog timeout
watchdog.setup(60000)


# firmware version to change and check after the FOTA procedure
fw_version = "v01"
# Reference table for no linear NTC sensor
ref_table = [329.5,247.7,188.5,144.1,111.3,86.43,67.77,53.41,42.47,33.90,27.28,22.05,17.96,14.69,12.09,10.00,8.313,
              6.940,5.827,4.911,4.160,3.536,3.020,2.588,2.228,1.924,1.668,1.451,1.266,1.108,0.9731,0.8572,0.7576]

def pub_event_handler():
    global ready
    while True:
        try:
            # Sync
            ready = True
            core_sample_lock.acquire()
            ready = False
            print("======== reading")
            # Read from 4-20mA channel1, resistive channel1, power channel1
            analog_val = board.read_420(1)
            temperature = board.read_resistive(1)
            print(" - temp:", temperature)
            print(" - analog:", analog_val)
            # Organize data in json dict
            to_send = {}
            to_send['temp'] = temperature
            to_send['analog'] = analog_val
            print("======== done")
            # Publish data to 4ZeroManager cloud service
            device.publish(to_send, "data")
            sleep(100)   
        except Exception as e:
            print('Publish exception: ', e)
            mcu.reset()

# remote color blink
def jblink(device, arg):
    if "led" in arg:
        if  arg["led"] in ['R', 'G', 'B', 'M', 'Y', 'C', 'W']:
            gpio.set(arg["led"],1)
            return {"res": "OK"}
        else:
            return {"error": "bad args"}

# remote async read sensor
def jread(device, arg):
    if "var" in arg:
        if arg["var"] == "analog":
            val = board.read_420(1)
        elif arg["var"] == "temp":
            val = board.read_resistive(1)
        else:
            val = "error"
        return {arg["var"]: val}

# custom jobs
my_jobs = {
    'blink': jblink,
    'read_async': jread,
}

try:
    # Let's connect to the wifi
    print("Connecting to WiFi...")
    wifi.configure(
            ssid=ssid,
            password=passwd)
    wifi.start()
    print("Connected...", wifi.info())
    print("Connecting to ZDM ...")
    #TODO: for tech team...remove host parameter before going in production   
    device = zdm.Agent(jobs={'blink': jblink, 'read_async': jread}, host="zmqtt.zdm.stage.zerynth.com")
    # connect the device to the ZDM
    device.start()
    print(print("Connected...", zdm.info()))
except Exception as e:
    print (e)
    mcu.reset()

core_sample_lock.acquire()
try:
    print("adc config...")
    # Config FourZeroBox ADC channels        
    board.config_adc(board.ADC_010_420, 1, 2, 7)
    board.config_adc(board.ADC_RES, 1, 2, 7)
    # Config FourZeroBox ADC conversion parameters
    board.set_conversion_010_420(1, 0, 100, 0, 0, 100)   
    board.set_conversion_resistive(1, -50, ref_table, 5)
    print("adc config done")
except Exception as e:
    print(e)
    mcu.reset()

try:
    print("core init done")
    # Start read_event_handler thread
    thread(pub_event_handler)
    print('start main')
    # Main Loop
    while True:
        print("Hello! firmware running version", fw_version)
        sleep(10000)
        # Sync between main thread and pub_event_handler thread 
        if ready:
            core_sample_lock.release()
            # Reset Watchdog timer
            watchdog.kick()
except Exception as e:
    print (e)
    mcu.reset()