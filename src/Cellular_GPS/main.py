################################################################################
# ZDM Cellular with GPS
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
# Before executing this code, please associate the device with your
# ZDM account by selecting "ZDM target" in VSCode Control Panel.

# Let's import the zdm module
from zdm import zdm
# We also need cellular or ethernet
from networking import cellular

# Globals
position = (0.0, 0.0, 0.0, 0.0, 0, 0.0, 0.0, 0.0, 0)

# Initialize the board
board.init()

# Uncomment the following to use the EXP-Connect board with ZM1-DB
# This adds the EXP-Connect as expansion and initialize the board.
#board.next_expansion(connect, (0,))

print("configuring cellular...")
cellular.configure()

print("initializing cellular gnss submodule...")
cellular.gnss.start()

# The very first GNSS fix can take some time since the
# hardware module has to lock all the required satellites.
# Here is the initial fix with long timeout.
print("Doing the initial GPS fix (up to 120secs)...")
try:
    position = cellular.gnss.fix(timeout=120)
except GNSSTimeoutError:
    print("Initial gps fix timed out")
except Exception as e:
    print("GNSS fix error: ", e)

while True:

    try:
        # Let's connect to the cellular
        print("connecting to cellular...")
        cellular.start()
        print("connected!",cellular.info())
        print("cellinfo: ",cellular.cellinfo())

        # the Agent class implements all the logic to talk with the ZDM
        # By setting the cellular_source and gnss_source, the ZDM agent
        # periodically sends to the cloud GSM cell and GPS position informations.
        # GSM and GPS data are visualized on the Cloud UI in the device section.
        agent = zdm.Agent(cellular_source=cellular, gnss_source=cellular.gnss)
        # just start it
        agent.start()

        # Parameters for adaptive GPS fix timeout
        c = 0        # counter
        k = 5        # increment in seconds for adaptive timeout
        max_incr = 4 # max increment steps for timeout
        while True:
            # Try to get GPS position with an adaptive fix timeout
            tout = 10+min(max_incr, c)*k  # linear increment with ceiling
            try:
                position = cellular.gnss.fix(timeout=tout)
                print("fixinfo: ", position)
                c = 0
            except GNSSTimeoutError:
                print("gps fix timed out: ", tout)
                c += 1
            except Exception as e:
                print("GNSS fix error: ", e)

            fixinfo = {}
            fixinfo['lat']   = position[0] # Latitude expressed as (-)dd.ddddd degrees
            fixinfo['lon']   = position[1] # Longitude expressed as (-)ddd.ddddd degrees
            fixinfo['hprec'] = position[2] # Horizontal dilution of precision
            fixinfo['alt']   = position[3] # Altitude above/below mean sea level, expressed in meters.
            fixinfo['mode']  = position[4] # GNSS positioning mode (2D, 3D)
            fixinfo['cog']   = position[5] # Course Over Ground
            fixinfo['kmh']   = position[6] # Speed over ground, expressed as Km/h.
            fixinfo['knt']   = position[7] # Speed over ground, expressed as knots.
            fixinfo['nsat']  = position[8] # Number of fixed satellites.

            # use the agent to publish values to the ZDM
            # Just open the device page from VSCode and check that data is incoming
            agent.publish(fixinfo, "fix")
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

