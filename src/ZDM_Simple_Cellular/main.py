################################################################################
# ZDM Simple Cellular
################################################################################

# First, import the board module from the bsp (board support package).
# The bsp loads board specific names, variables and settings so that
# this project can be run on different Zerynth hardware
# without changing a line of code.
from bsp import board

# Import the serial interface to talk with the cellular module.
import serial

# The Zerynth Device Manager is the entrypoint for the zCloud.
# Let's connect and send data to the ZDM with a simple example.
# Before exeuting this code, please associate the device with your
# ZDM account by selecting "ZDM target" in VSCode Control Panel.

# Let's import the zdm module
from zdm import zdm
# We also need cellular or ethernet
from networking import cellular


# Initialize the board
board.init()

# Open and configure the cellular serial port
_ = serial.serial(SERIAL1, baud=115200)
modem = serial.serial(SERIAL2, baud=115200, flow_ctrl=serial.HW_FLOWCTRL_DISABLE)

while True:

    try:
        # Let's connect to the cellular
        print("configuring cellular...")
        cellular.configure(modem)
        print("connecting to cellular...")
        cellular.start()
        print("connected!",cellular.info())

        # the Agent class implements all the logic to talk with the ZDM
        agent = zdm.Agent()
        # just start it
        agent.start()

        while True:
            # use the agent to publish values to the ZDM
            # Just open the device page from VSCode and check that data is incoming
            agent.publish({"value":random(0,100)}, "test")
            sleep(5000)
            # The agent automatically handles connections and reconnections
            print("ZDM is online:    ",agent.online())
            # And provides info on the current firmware version
            print("Firmware version: ",agent.firmware())

        cellular.stop()
        print("disconnected from cellular")
    except CellularBadAPN:
        print("Bad APN")
        cellular.stop()
        cellular.deinit()
    except CellularModemInitError:
        print("Modem initialization failed")
        cellular.deinit()
    except CellularException:
        print("Generic Cellular Exception")
        cellular.stop()
        cellular.deinit()
    except Exception as e:
        print("Exception: ", e)
        raise e

    sleep(3000)

