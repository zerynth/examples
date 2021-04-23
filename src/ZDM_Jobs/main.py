################################################################################
# ZDM Agent
################################################################################

# The Zerynth Device Manager is the entrypoint for the zCloud.
# Let's connect and send data to the ZDM with a simple example.
# Before exeuting this code, please associate the device with your
# ZDM account by selecting "ZDM target" in VSCode Control Panel.

from bsp import board
# Let's import the zdm module
from zdm import zdm
# We also need wifi or ethernet
from networking import wifi
import gpio


# Set the ssid and password of your wifi network
ssid = "ZerynthTest"
passwd = "ZerynthTT"


# this is a function callable by the ZDM with a job request.
# Notice that it has two parameters: the ZDM agent that receives the request
# and a dictionary with the arguments of the job.
# Color just switches the onboard RGB led to the value set in the job request
def color(agent, args):
    print("Job request received!",args)
    if not "color" in args:
        return {"msg": "Invalid argument for color job"}

    c = args["color"]
    if c=="red":
        gpio.set(LED_GREEN,1)
        gpio.set(LED_BLUE,1)
        gpio.set(LED_RED,0)
    elif c=="green":
        gpio.set(LED_GREEN,0)
        gpio.set(LED_BLUE,1)
        gpio.set(LED_RED,1)
    elif c=="blue":
        gpio.set(LED_GREEN,1)
        gpio.set(LED_BLUE,0)
        gpio.set(LED_RED,1)
    else:
        gpio.set(LED_GREEN,1)
        gpio.set(LED_BLUE,1)
        gpio.set(LED_RED,1)
        c="off"

    return {"msg": "LED set to %s" % c}

while True:

    try:
        # Let's connect to the wifi
        print("configuring wifi...")
        wifi.configure(
            ssid=ssid,
            password=passwd)
        print("connecting to wifi...")
        wifi.start()
        print("connected!",wifi.info())

        # the Agent class implements all the logic to talk with the ZDM
        # it also accepts a dictionary of functions to be called as jobs
        agent = zdm.Agent(jobs={"color":color})
        # just start it
        agent.start()

        while True:
            # use the agent to publish values to the ZDM
            # Just open the device page from VSCode and check that data is incoming
            v = random(0,100)
            agent.publish({"value":v}, "test")
            print("Published",v)
            sleep(5000)
            # The agent automatically handles connections and reconnections
            print("ZDM is online:    ",agent.online())
            # And provides info on the current firmware version
            print("Firmware version: ",agent.firmware())

        wifi.stop()
        print("disconnected from wifi")
    except WifiBadPassword:
        print("Bad Password")
    except WifiBadSSID:
        print("Bad SSID")
    except WifiException:
        print("Generic Wifi Exception")
    except Exception as e:
        raise e

    sleep(3000)

