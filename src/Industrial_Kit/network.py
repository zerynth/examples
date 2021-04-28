import utils as ut                                  # utility functions
from networking import wifi
import mcu

def connect(ssid, password):
    for attempt in range(0,4):
        try:
            # LED feedback
            if attempt == 0:
                ut.set_white()
            else:
                ut.set_blue()       
            # Connection to wifi network
            print("2 - Connecting to wifi ...")
            wifi.configure(ssid, password)
            wifi.start()
            print("... connected!", wifi.info())
            # Once connected exit from cycle
            break    
        except Exception as e:
            print ("Connect to wifi failed: ", e)
            wifi.stop()
            sleep(1000)
    else:
        print ("Network initialization fatal error: ")
        ut.set_red()
        sleep(1000)
        mcu.reset()