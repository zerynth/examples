import gpio

import time
import gc
import utils
import mcu
import timers
import threading as th

from bsp import board

# Uncomment the following to use the EXP-CONNECT board with ZM1-DB
#from expansions import connect

from zdm import zdm
from networking import cellular
from networking import socket

# This project utilities
import utils

# Initialize the board
board.init()

# Uncomment the following to use the EXP-Connect board with ZM1-DB
# This adds the EXP-Connect as expansion and initialize the board.
#board.next_expansion(connect, (0,))

gnss = cellular.gnss # shortcut

fix_polling_time = 35000  # milliseconds
cell_polling_time = 30000 # milliseconds

fix_time = 0
rssi = 99
location = (0.0, 0.0, 0.0, 0.0, 0, 0.0, 0.0, 0.0, 0)
fixed = False
cell = ("","","","",0,0,0,0)
cnt = 0
recon_cnt = 5
cellularstart_retry_max = 10

# Thread which periodically gets GPS fix data
def gps_fix():
    global location, fix_time, fixed
    c = 0
    k = 5        # increment in seconds for adaptive timeout
    max_incr = 4 # max increment steps for timeout
    while True:
        sleep(fix_polling_time)
        start = time.time()
        tout = 10+min(max_incr,c)*k
        try:
            print("getting gps location. timeout: ", tout)
            location = gnss.fix(timeout=tout)
            c = 0
            fixed = True
        except Exception as e:
            print("gps fix timed out: ", e, c)
            c += 1
            fixed = False
        fix_time = time.time() - start
        print("location: %s, fix_time: %d" % (location, fix_time))
        host = "www.google.com"
        ip=cellular.resolve(host)
        print("resolved ip: ", ip, host)

# Thread which periodically gets cell tower data
def cell_info():
    global rssi, cell
    while True:
        sleep(cell_polling_time)
        try:
            _rssi = cellular.rssi()
            _cell = cellular.cellinfo()
            rssi = _rssi
            cell = _cell
        except Exception as e:
            print("cellular rssi/cellinfo get failed: ", e)

print("=== LED codes ===")
print("Steady white: initialization")
print("Off: initialization done")
print("Blue blink: cellular is connecting or connection lost")
print("Green blink: cellular connection ok, GPS fix ok")
print("Yellow blink: cellular connection ok, GPS not fixed")
print("=================")

try:
    print("configuring...")
    cellular.configure()  # zSIM

    # white LED during init
    gpio.set(LED_GREEN,0)
    gpio.set(LED_BLUE,0)
    gpio.set(LED_RED,0)

    print("Initializing modem...")
    cellular.init()
    print("Initializing cellular gnss submodule...")
    gnss.start()

    # The very first GNSS fix can take some time since the
    # hardware module has to lock all the required satellites.
    # Here is the initial fix with long timeout.
    print("Doing the initial GPS fix (up to 60secs)...")
    try:
        location = gnss.fix(timeout=60)
        fixed = True
    except Exception as e:
        print("Initial gps fix timed out: ", e)
        fixed = False

    # Retry cellular connection otherwise reboot
    for _ in range(3):
        try:
            print("Connecting to cellular...")
            cellular.start()
            print("connected!", cellular.info())
            break
        except Exception as e:
            print("cellular err", e)
    else:
        print("Can't connect cellular, resetting")
        mcu.reset()

    # the Agent class implements all the logic to talk with the ZDM
    agent = zdm.Agent()
    print("agent")
    # just start it
    agent.start()
    while not agent.online():
        print("not online")
        sleep(1000)

    print("agent started")

    now = time.now()
    agent.publish({"bts":now}, "B")

    # Start GPS and cellinfo threads
    thread(gps_fix)
    thread(cell_info)

    stat_free_ram = utils.StatVar()
    stat_ms_since = utils.StatVar()
    stat_frag_perc = utils.StatVar()
    stat_allocated = utils.StatVar()
    stat_free_blocks = utils.StatVar()

    pub_err = 0
    publish_period = 60
    ts_last_publish = 0
    cnt = 0
    p = 0
    cell_cnt = 0
    conn_restart_cnt = 0

    reading_lock = th.Lock()
    reading_lock.acquire()
    timers.Timer().interval(1000, reading_lock.release)

    # Init ok -> switch the LED off
    gpio.set(LED_GREEN,1)
    gpio.set(LED_BLUE,1)
    gpio.set(LED_RED,1)

    while True:
        # use the agent to publish values to the ZDM
        # Just open the device page from VSCode and check that data is incoming
        reading_lock.acquire()
        cnt+=1

        now = time.now()
        print("now", now)

        # Get memory allocation stats
        gc_info = gc.info()
        print("gc_info", gc_info)
        # 0. Total memory in bytes
        # 1. Free memory in bytes
        # 2. Memory fragmentation percentage
        # 3. Number of allocated blocks
        # 4. Number of free blocks
        # 5. GC Period: milliseconds between forced collections
        # 6. Milliseconds since last collection

        stat_free_ram.add(gc_info[1])
        stat_frag_perc.add(gc_info[2])
        stat_allocated.add(gc_info[3])
        stat_free_blocks.add(gc_info[4])

        stat_ms_since.add(gc_info[-1])

        ts_send = utils.get_publish_ts(now, publish_period, ts_last_publish)
        stats = agent.mqtt.stats()
        print("stats", stats)

        if ts_send:
            try:
                p+=1

                # system stats
                to_send = {}
                to_send['ts'] = ts_send
                to_send['f'] = stat_free_ram.get()
                to_send['ms'] = stat_ms_since.get()
                to_send['e'] = pub_err
                to_send['c'] = cnt
                to_send['p'] = p
                to_send['mq'] = stats
                to_send['g2'] = stat_frag_perc.get()
                to_send['g3'] = stat_allocated.get()
                to_send['g4'] = stat_free_blocks.get()

                # GPS data
                to_send['lat'] = location[0]
                to_send['lon'] = location[1]
                to_send['h_prec'] = location[2]
                to_send['alt'] = location[3]
                to_send['fix_type'] = location[4]
                to_send['cog'] = location[5]
                to_send['speedkm'] = location[6]
                to_send['nsat'] = location[8]
                to_send['fixtm'] = fix_time

                # Cellular data
                to_send['rssi'] = rssi

                to_send['state'] = cell[0]
                to_send['act'] = cell[1]
                to_send['opcode'] = cell[2]
                to_send['band'] = cell[3]
                to_send['chan'] = cell[4]
                to_send['lac'] = cell[5]
                to_send['cellid'] = cell[6]
                to_send['bsic'] = cell[7]
                to_send['oper'] = cell[10]

                cnt = 0

                try:
                    host="now.zerynth.com"
                    ip=cellular.resolve(host)
                    print("resolved ip: ", ip, host)
                    if ip != None:
                            s = socket.socket()
                            print("connecting socket...")
                            try:
                                s.connect((ip,80))
                                s.send("GET / HTTP/1.1\n",15,0,0)
                                s.send("Host: now.zerynth.com\n\n",23,0,0)
                                b = s.recv(256)
                                print(b)
                                b=""
                            except Exception as e:
                                print("socket transmission error", e)
                                s.close()
                                b=""

                            print(b)
                            print("close socket...")
                            s.close()
                except Exception as e:
                    print("http socket err: ", e)

                print("to_send: ", to_send)
                agent.publish(to_send, "INFO")

                # The agent automatically handles reconnections
                print("ZDM is online:    ",agent.online())
                # # And provides info on the current firmware version
                print("Firmware version: ",agent.firmware())
                ts_last_publish = ts_send
            except Exception as e:
                print("publish err", e)
                pub_err +=1
                conn_restart_cnt += 1

            # Restart cellular connection upon to many 
            # failed reconnection attempts
            if conn_restart_cnt >= recon_cnt:
                conn_restart_cnt = 0
                cellular.stop()
                c = 0
                while c <= cellularstart_retry_max:
                    sleep(5000)
                    try:
                        c += 1
                        print("Try to restart cellular connection. retry:", c)
                        cellular.start()
                        break
                    except Exception as e:
                        print("cellular.start failed with error ", e)
                        if c >= cellularstart_retry_max:
                            print("Reached max cellular restart attempts:", c)
                            raise e
                agent.start()


            # Blue LED: No connection
            gpio.set(LED_BLUE,0)
        else:
            # Green LED: connection ok, GPS fixed
            gpio.set(LED_GREEN,0)
            if not fixed:
                # Yellow LED: connection ok, GPS not fixed
                gpio.set(LED_RED,0)

        sleep(50)
        gpio.set(LED_BLUE, 1)
        gpio.set(LED_GREEN, 1)
        gpio.set(LED_RED, 1)


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

mcu.reset()
