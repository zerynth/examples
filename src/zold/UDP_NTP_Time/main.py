# UDP NTP Time
# Created at 2019-02-19 08:07:55.144570

import streams
import socket

# import the wifi interface
from wireless import wifi

# the wifi module needs a networking driver to be loaded
# in order to control the board hardware.
# This example can be used as is with ESP32 based devices
from espressif.esp32net import esp32wifi as wifi_driver


def ntc_ts_to_datetime(t):
    # convert NTP timestamp (seconds since January 1st 1900) to datetime formatted string
    # YYYY-mm-dd HH:MM:SS
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
    streams.serial()

    # init the wifi driver!
    # The driver automatically registers itself to the wifi interface
    # with the correct configuration for the selected board
    wifi_driver.auto_init()

    # use the wifi interface to link to the Access Point
    # change network name, security and password as needed
    print("Establishing WiFi Link...")
    for retry in range(5):
        try:
            # FOR THIS EXAMPLE TO WORK, "Network-Name" AND "Wifi-Password" MUST BE SET
            # TO MATCH YOUR ACTUAL NETWORK CONFIGURATION
            wifi.link("Network-Name",wifi.WIFI_WPA2,"Wifi-Password")
            print("...done!")
            break
        except Exception as e:
            pass
    else:
        print(":( can't connect to wifi")
        raise IOError

    # create an UDP socket and set a timeout of 1 second
    sock = socket.socket(type=socket.SOCK_DGRAM)
    sock.settimeout(1000)

    # create an NTP request packet
    pkt = bytearray([0]*48)
    pkt[0] = 0x1B

    while True:
        try:
            # resolve the NTP server hostname to get its IP address
            ip_string = wifi.gethostbyname("0.pool.ntp.org")
            ip = socket.ip_to_tuple(ip_string)

            # create a tuple containing NTP server ip address and port
            addr = (ip[0], ip[1], ip[2], ip[3], 123)

            print("Sending NTP request to %s:%d" %(ip_string, 123))
            # send the NTP request packet to the NTP server
            sock.sendto(pkt, addr)

            # read the response from the server
            res = sock.recv(48)

            # extract the "transmit timestamp" field from the received packet
            ts =  (res[40]<<24) | (res[41]<<16) | (res[42]<<8) | res[43]

            # convert NTP timestamp to human readable datetime
            print(" >", ntc_ts_to_datetime(ts))
            print(" ")
        except Exception as e:
            print(" >", e)
        sleep(10000)

except Exception as e:
    print(e)
