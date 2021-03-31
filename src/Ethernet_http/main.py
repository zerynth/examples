################################################################################
# Ethernet HTTP
################################################################################

from bsp import board

from networking import eth
from networking import socket

board.init()
board.summary()

ifc=-1

while True:

    try:
        print("configuring...")
        ifc = eth.configure(dhcp=True)
        print("connecting...")
        eth.start()

        print("connected...")
        print("info...")
        print(eth.info())
        ip=eth.resolve("now.zerynth.com")
        print("resolved",ip)
        if (ip != None):
            print("creating socket...")
            s = socket.socket(ifc=ifc)
            print("connecting socket...")
            s.connect((ip,80))
            s.send("GET / HTTP/1.1\n")
            s.send("Host: now.zerynth.com\n\n")
            b = s.recv(256)
            print(b)
            print("close socket...")
            s.close()
        print("disconnecting...")
        eth.disconnect()
        print("disconnected...")
    except ConnectionError:
        print("Ethernet Connection Exception")
    except ConnectionTimeoutError:
        print("Ethernet Connection Timeout Exception")
    except ResolveError:
        print("Resolv error Exception")
    except NetworkGenericError:
        print("Generic Ethernet Exception")
    except Exception as e:
        raise e

    sleep(3000)