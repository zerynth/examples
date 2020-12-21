################################################################################
# NTPClient using UDP
#
# Created: 2019-06-16
# Author: L. Marsicano
################################################################################

import streams
import ntpclient 

streams.serial()

# import the wifi interface
from wireless import wifi

# the wifi module needs a networking driver to be loaded
# in order to control the board hardware.
# This example can be used as is with ESP32 based devices
from espressif.esp32net import esp32wifi as wifi_driver
def ntc_ts_to_datetime(t):
   ts = t - 2208988800
    
   s = ts % 60
   ts //= 60
   m = ts % 60
   ts //= 60
   h = ts % 24
   ts //= 24

   a = (4 * ts + 102032) // 146097 + 15
   b = (ts + 2442113 + a - (a//4))
   c = (20 * b - 2442) // 7305
   d =  b - 365* c - (c // 4)
   e = d * 1000 //30601
   f = d - e*30 - e*601//1000

   if e <= 13:
       c-=4716
       e -= 1
   else:
       c -= 4715
       e -= 13

   Y = c
   M = e
   D = f

   return "%d-%02d-%02d %02d:%02d:%02d"%(Y, M, D, h, m, s)

try:
    wifi_driver.auto_init()
    for i in range(0, 5):
        try:
            # Change this line to match your network configuration
            wifi.link("SSID",wifi.WIFI_WPA2,"PASSWORD")
            break
        except Exception as e:
            print(e)
            sleep(500)
    else:
        print("Could not link :(")
        raise IOError

    client = ntpclient.NTPClient(wifi_driver)
    t = client.get_time()
    print("Time is", t)
    print("Converted time is:", ntc_ts_to_datetime(t))
except Exception as e:
    print(e)

