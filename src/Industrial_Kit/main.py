###############################################################################
# Industrial IoT Kit-IO
###############################################################################

from bsp import board
from zdm import zdm
import mcu
import init.inputs as io
import utils as ut
import reading
import network

# Init
board.init()
board.summary()

# Connection to wifi
ssid = "Example-SSID"
password = "Example-Password"
network.connect(ssid, password)

# Connection to ZDM
print("3 - Connecting to zDeviceManager ...")
agent = zdm.Agent()
print("4 - Agent created!")
agent.start()



try:
    print("######################################")
    # Start reading thread
    thread(reading.read_loop, agent)
    ut.set_green()
    while True:
        ut.set_blink(LED_GREEN, 100, 900)
except Exception as e:
    ut.set_red()
    sleep(1000)
    mcu.reset()
