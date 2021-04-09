################################################################################
# WiFi http
################################################################################

from networking import wifi
from networking import socket

# Set the ssid and password of your wifi network
ssid = "ZerynthTest"
passwd = "ZerynthTest"

while True:
    try:
        # Let's connect to the wifi
        print("configuring...")
        wifi.configure(
                ssid=ssid,
                password=passwd)
        print("connecting...")
        wifi.start()
        print("connected...")
        print("info ", wifi.info())
        ip=wifi.resolve("now.zerynth.com")
        print("resolved",ip)
        # Let's create a socket
        print("creating socket...")
        s = socket.socket()
        print("connecting socket...")
        s.connect((ip, 80))
        # Let's send an HTTP request
        print("sending HTTP request...")
        s.send("GET / HTTP/1.1\n")
        s.send("Host: now.zerynth.com\n\n")
        # Let's read an HTTP response
        b = bytearray(1)
        rb = 1
        result = []
        s.settimeout(4000)
        while rb>0:
            try: 
                rb = s.recv_into(b)
                result.append(b.copy())
            except Exception as e:
                rb = 0
        print("result...")
        print(''.join([str(elem) for elem in result]))
        print("close socket...")
        s.close()
        wifi.stop()
        print("disconnected...")
    except WifiBadPassword:
        print("Bad Password")
    except WifiBadSSID:
        print("Bad SSID")
    except WifiException:
        print("Generic Wifi Exception")
    except Exception as e:
        raise e

    sleep(3000)