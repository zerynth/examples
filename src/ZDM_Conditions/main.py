################################################################################
# ZDM Agent
################################################################################

# The Zerynth Device Manager is the entrypoint for the zCloud.
# Let's connect and send data to the ZDM with a simple example.
# Before exeuting this code, please associate the device with your
# ZDM account by selecting "ZDM target" in VSCode Control Panel.

# First, import the board module from the bsp (board support package).
# The bsp loads board specific names, variables and settings so that
# this project can be run on different Zerynth hardware
# without changing a line of code.
from bsp import board

# Let's import the zdm module
from zdm import zdm
# We also need wifi or ethernet
from networking import wifi
import gpio


# Set the ssid and password of your wifi network
ssid = "ZerynthTest"
passwd = "ZerynthTT"


# this function is executed when the agent receives the list of the open conditions from a previous run.
# Being able to retrieve the open conditions is very useful in cases like power loss. Upon restart the firmware
# will known where it left from.
# In this example, we close all the open conditions from the previous run
def my_open_conditions_callback(agent, conditions):
    print("Received open conditions:", len(conditions))
    for c in conditions:
        print("CLOSING ", c)
        c.close()


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
        # it also accepts an array of label with the type of conditions handled by the firmware.
        # It also needs a function to be called when the list of already open conditions are received.
        #TODO: for tech team...remove host parameter before going in production
        agent = zdm.Agent(conditions=["battery"],
                on_conditions=my_open_conditions_callback,
                host="zmqtt.zdm.stage.zerynth.com")
        # just start it
        agent.start()

        while True:
            # Let's create some conditions for tracking the battery status
            infoLevel = agent.new_condition("battery")
            warningLevel = agent.new_condition("battery")
            criticalLevel = agent.new_condition("battery")
            fatalLevel = agent.new_condition("battery")

            # Let's also request the open conditions to the agent.
            # When they are received, they will be passed to my_open_conditions_callback
            agent.request_conditions()

            # store the initial battery level (100%)
            battery_lvl_curr = 100
            # store the previous  battery level
            battery_lvl_prv = 100

            # indicate if the battery is in the recharge state (True) or not (False)
            recharge = False
            done = False

            while not done:
                # The agent automatically handles connections and reconnections
                print("ZDM is online:    ",agent.online())
                # And provides info on the current firmware version
                print("Firmware version: ",agent.firmware())
                # Print the battery level
                print("Battery level:", battery_lvl_curr)
                # Check the battery level and update the conditions accordingly
                # Conditions are displayed in the ZDM device page
                # accessible from VSCode (device page)
                if battery_lvl_curr > 80:
                    if recharge and infoLevel.is_open():
                        print("[INFO] close condition")
                        infoLevel.close({"status": "INFO", "lvl": battery_lvl_curr})
                        done = True

                elif 60 < battery_lvl_curr <= 80:
                    if not recharge and not infoLevel.is_open():
                        print("[INFO] open condition")
                        infoLevel.open({"status": "INFO", "lvl": battery_lvl_curr})
                    else:
                        if warningLevel.is_open():
                            print("[WARNING] close condition")
                            warningLevel.close({"status": "WARNING", "lvl": battery_lvl_curr})

                elif 40 < battery_lvl_curr <= 60:
                    if not recharge and not warningLevel.is_open():
                        print("[WARNING] open condition")
                        warningLevel.open({"status": "WARNING", "lvl": battery_lvl_curr})
                    else:
                        if criticalLevel.is_open():
                            print("[CRITICAL] close condition")
                            criticalLevel.close({"status": "CRITICAL", "lvl": battery_lvl_curr})

                elif 20 < battery_lvl_curr <= 40:
                    if not recharge and not criticalLevel.is_open():
                        print("[CRITICAL] open condition")
                        criticalLevel.open({"status": "CRITICAL", "lvl": battery_lvl_curr})
                    else:
                        if fatalLevel.is_open():
                            print("[FATAL] close condition")
                            fatalLevel.close({"status": "FATAL", "lvl": battery_lvl_curr})

                elif 10 < battery_lvl_curr <= 20:
                    if not recharge and not fatalLevel.is_open():
                        print("[FATAL] open condition")
                        fatalLevel.open({"status": "FATAL", "lvl": battery_lvl_curr})

                elif 0 < battery_lvl_curr <= 10:
                    print("Recharging battery...")
                    recharge = True

                battery_lvl_prv = battery_lvl_curr
                if recharge:
                    battery_lvl_curr = battery_lvl_curr + 5
                else:
                    battery_lvl_curr = battery_lvl_curr - 5

                sleep(2000)

        wifi.stop()
        print("disconnected from wifi")
    except WifiBadPassword:
        print("Bad Password")
    except WifiBadSSID:
        print("Bad SSID")
    except WifiException:
        print("Generic Wifi Exception")
    except Exception as e:
        print(e)

    sleep(3000)

