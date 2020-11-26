################################################################################
# RTC Keep Time
#
# Created by Zerynth Team 2018 CC
# Authors: G. Baldi, L. Rizzello
################################################################################

import streams
import json
import requests

from wireless import wifi
# import a wifi driver to connect and retrieve base timestamp
from espressif.esp32net import esp32wifi as wifi_driver

# import Real-Time Clock module
import rtc

def get_epoch():
    user_agent = {"user-agent": "curl/7.56.0"}
    return int(json.loads(requests.get("http://now.zerynth.com/", headers=user_agent).content)['now']['epoch'])

streams.serial()
wifi_driver.auto_init()

print('connecting to wifi...')
try:
    wifi.link("SSID",wifi.WIFI_WPA2,"PSW")
except Exception as e:
    print("ooops, something wrong while linking :(", e)
    while True:
        sleep(1000)

timestamp = get_epoch()
rtc.set_utc(timestamp)
while True:
    tm = rtc.get_utc()
    print(tm.tv_seconds)
    print(tm.tm_year,'/',tm.tm_month,'/',tm.tm_mday,sep='')
    print(tm.tm_hour,':',tm.tm_min,':',tm.tm_sec,sep='')
    sleep(1000)

