################################################################################
# ZDM Simple Cellular
################################################################################

# First, import the board module from the bsp (board support package).
# The bsp loads board specific names, variables and settings so that
# this project can be run on different Zerynth hardware
# without changing a line of code.
from bsp import board

# Uncomment the following to use the EXP-CONNECT board with ZM1-DB
#from expansions import connect

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

# Uncomment the following to use the EXP-Connect board with ZM1-DB
# This adds the EXP-Connect as expansion and initialize the board.
#board.next_expansion(connect, (0,))

print("configuring cellular...")
cellular.configure()

while True:

    try:
        # Let's connect to the cellular
        print("connecting to cellular...")
        cellular.start()
        print("connected!",cellular.info())
        print("www.zerynth.com: ", cellular.resolve("www.zerynth.com"))

        # the Agent class implements all the logic to talk with the ZDM
        agent = zdm.Agent()
        # just start it
        agent.start()

        while True:
            # Get the cellular current cell informations
            ci = cellular.cellinfo()
            print("cellinfo: ", ci)

            # Prepare the massage to be sent to ZDM
            msg = {}
            msg['state']  = ci[0]  # Connection state
            msg['act']    = ci[1]  # Access technology
            msg['opcode'] = ci[2]  # Operator code
            msg['band']   = ci[3]  # Selected band
            msg['chan']   = ci[4]  # Channel ID
            msg['lac']    = ci[5]  # Local Area Code
            msg['cellid'] = ci[6]  # Cell ID
            msg['bsic']   = ci[7]  # Base station ID code
            msg['mcc']    = ci[8]  # MCC
            msg['mnc']    = ci[9]  # MNC
            msg['oper']   = ci[10] # Operator name

            # use the agent to publish values to the ZDM
            # Just open the device page from VSCode and check that data is incoming
            agent.publish(msg, "cellinfo")
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

