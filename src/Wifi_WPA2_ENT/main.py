################################################################################
# WiFi http
################################################################################

# First, import the board module from the bsp (board support package).
# The bsp loads board specific names, variables and settings so that
# this project can be run on different Zerynth hardware
# without changing a line of code.
from bsp import board

from networking import wifi

ssid = "Example-SSID"
# Add enterprise user and password
ent_user="Test_USR",
ent_pwd="Test_PWD"

while True:
    try:
        # Let's connect to the wifi
        print("configuring...")
        wifi.configure(
                ssid=ssid,
                security=wifi.WPA2_ENTERPRISE,
                ent_user=ent_user,
                ent_pwd=ent_pwd)
        print("connecting...")
        wifi.start()
        print("connected...")
        print("info", wifi.info())
        # Resolve a host name
        ip=wifi.resolve("now.zerynth.com")
        print(ip)
        wifi.stop()
        print("disconnected...")
    except WifiBadSSID:
        print("Bad SSID")
    except WifiBadAuth:
        print("Bad User or User Password")
    except WifiException:
        print("Generic Wifi Exception")
    except Exception as e:
        raise e

    sleep(3000)