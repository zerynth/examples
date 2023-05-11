################################################################################
# ZDM Agent for on premise installation
################################################################################

# The Zerynth Device Manager is the entrypoint for the zCloud.
# Let's connect and send data to the ZDM with a simple example.
# Before executing this code, please associate the device with your
# ZDM account by selecting "ZDM target" in VSCode Control Panel.

from bsp import board
# Let's import the zdm module
from zdm import zdm
# We also need wifi or wifiernet
from networking import wifi
# We load the SSL Certification Authorty (CA) certificate from a file
import fs
# We create a custom SSL context
import ssl

board.init()
board.summary()

# Set the ssid and password of your wifi network
ssid = "Zerynth"
passwd = "Zerynth3"

# Let's connect to the wifi
print("configuring wifi...")
wifi.configure(ssid=ssid, password=passwd)
print("connecting to wifi...")
wifi.start()
print("connected!",wifi.info())

# Let's load the CA from file. It is in the 'resources' project folder
try:
    f = fs.open("/zerynth/zdm.ca.pem", "r")
    cacert = f.read()
    f.close()
except Exception as e:
    print("error reading zdm ca", e)
    cacert=""

# Create the SSL context to be passeed to the Agent
ctx = ssl.context(cacert=cacert, verify=True, secure_element=True)

# Build the URLs to be passed to the Agent
domain="onprem.example.com"
zdm_host="zmqtt.zdm."+domain
zdm_upload_host="uploads.zdm."+domain

while True:

    try:

        # set the binary blobs upload url in the agent config object
        agent_config = zdm.Config(upload_host=zdm_upload_host)

        # The Agent class implements all the logic to talk with the ZDM.
        # It also accepts a dictionary of functions to be called as jobs.
        # Here we set the zdm and upload URLs, aside of the custom SSL context.
        agent = zdm.Agent(host=zdm_host, cfg=agent_config, ssl_ctx=ctx)

        # just start it
        agent.start()

        while True:
            # use the agent to publish values to the ZDM
            # Just open the device page from VSCode and check that data is incoming
            agent.publish({"value":random(0,100)}, "test")
            # The agent automatically handles connections and reconnections
            print("ZDM is online:    ",agent.online())
            # And provides info on the current firmware version
            print("Firmware version: ",agent.firmware())
            sleep(10000)

    except Exception as e:
        print("Error:",e)
        continue
        raise e

    sleep(3000)

