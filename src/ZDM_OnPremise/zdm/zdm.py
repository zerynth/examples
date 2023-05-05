from networking import net
from protocols import http
from protocols import mqtt
from protocols import ntp
from crypto import element
import fs
import json
import mcu
import ssl
import time
import timers
from zdm import zfota as zfota
from zdm import zfs as zfsm


ZDM_RESET_REASON_UNKNOWN=0
ZDM_RESET_REASON_JOB=1
ZDM_RESET_REASON_FOTA=2
ZDM_RESET_REASON_FOTA_REVERT=3
ZDM_RESET_REASON_ZFS=4
ZDM_RESET_REASON_CUSTOM=5

class Config():
    def __init__(self,
                 keepalive=60,
                 reconnect_after=5000,
                 network_timeout=60000,
                 clean_session=True,
                 qos_publish=1,
                 qos_subscribe=1,
                 fota_http_timeout=5000,
                 upload_host="uploads.zdm.zerynth.com"):
        self.keepalive = keepalive
        self.network_timeout = network_timeout
        self.reconnect_after = reconnect_after
        self.sock_keepalive = [1, 10, 5]
        self.clean_session = clean_session
        self.qos_publish = qos_publish
        self.qos_subscribe = qos_subscribe
        self.fota_http_timeout = fota_http_timeout
        self.upload_host = upload_host


def __job_reset(obj, arg):
    return 'resetting device...'


class Agent:
    def __init__(self, cfg=None,
                 jobs={},
                 set_clock_every=300,
                 on_fota=None,
                 on_zfs=None,
                 clock_source=None,
                 host="zmqtt.zdm.zerynth.com",
                 gnss_source=None,
                 cellular_source=None,
                 stats_source=None,
                 send_gnss_every=600,
                 send_cellular_every=600,
                 send_stats_every=600,
                 on_reset=None,
                 download_chunk_size=4096,
                 on_set_clock=None,
                 password=None,
                 secure=True,
                 devid=None,
                 no_tls=False,
                 ssl_ctx=()
                 ):
        # get configuration
        self._cfg = Config() if cfg is None else cfg

        # get credentials
        if devid and not secure:
            dcn=devid
        else:
            dcn = element.common_name()
        self.dcn=dcn

        self.th = None
        self.flag_first_connect = False
        self.flag_has_time = False

        # Get the current clock as last config time instead of setting it to 0.
        # On soft reset the system clock is not reset to 0,
        # the value is the time before the reset (with possible skews).
        # In such a case, setting the flag_last_config to 0 here creates huge
        # time delta when clock syncs.
        self.flag_last_config = time.now()

        if no_tls:
            self.ssl_ctx = ()
            port = 1883
        else:
            port = 8883
            if ssl_ctx:
                self.ssl_ctx = ssl_ctx
                zdebug("Using caller provided ssl ctx")
            else:
                if "stage" in host:
                    cacert = ZDM_CA_STAGE
                elif "test" in host:
                    cacert = ZDM_CA_TEST
                else:
                    cacert = ZDM_CA
                self.ssl_ctx = ssl.context(cacert=cacert, secure_element=secure, verify=secure)
        self.host=host
        passw=password
        self.token = password
        if secure:
            passw=dcn
        self.mqtt = mqtt.MQTT(
            host, dcn,
            username=dcn, password=passw,
            port=port,
            clean_session=self._cfg.clean_session,
            keepalive=self._cfg.keepalive,
            reconnect_after=self._cfg.reconnect_after,
            network_timeout=self._cfg.network_timeout,
            ctx=self.ssl_ctx)

        self.data_topic = 'j/data/'+dcn
        self.up_topic = 'j/up/'+dcn
        self.dn_topic = 'j/dn/'+dcn

        self.current = {}
        self.expected = {}

        # self._on_timestamp = on_timestamp
        self._set_clock = set_clock_every
        self._clock_source = clock_source or self.request_time

        self._gps_source = gnss_source
        self._send_gps_every = max(send_gnss_every, 120)
        self._last_gps_sent = 0

        self._cellular_source = cellular_source
        self._send_cellular_every = max(send_cellular_every, 60)
        self._last_cellular_sent = 0

        self._stats_source = stats_source
        self._send_stats_every = max(send_stats_every, 60)
        self._last_stats_sent = 0

        self._timer = timers.Timer()
        self._timer.interval(60000,self._periodic_callbacks)

        self._fota_callback = on_fota
        self._zfs_callback = on_zfs
        self._reset_callback = on_reset
        self._time_callback = on_set_clock
        self.jobs = {
            'reset': __job_reset
        }

        self.jobs.update(jobs)

        self.fota_ongoing = False
        # set subscribe and callbacks
        self.mqtt.on(self.dn_topic, self._handle_dn_msg, self._cfg.qos_subscribe)
        self.dl_chunk_size = download_chunk_size
        self.fota_percentage = [0, 0]
        self.fota_brate = 0

    def _connect(self):
        zinfo("Connecting...")
        zdebug("Using zdm host:",self.host)
        exc = None
        attempt = 0
        while True:
            try:
                zdebug("connection attempt", attempt)
                rc = self.mqtt.connect()
                zdebug("mqtt connected successfully", rc)
                self.flag_first_connect = True
                break
            except Exception as e:
                exc = e
                zwarn("connection error", e)
                attempt = attempt+1
                sleep(min((attempt)*1000, 30000))
        self._config()

    def _run(self):
        zinfo("Starting...")
        self._connect()
        self.mqtt.loop()

    def firmware(self):
        return zfota.current_version()

    def zfs(self):
        return zfsm.current_version()

    def start(self, wait_working=10):
        self.permanent_fota = zfota.is_permanent()
        if self.th is None:
            self.th = thread(self._run)
        for attempt in range(wait_working):
            if not self.online():
                zdebug("agent not working yet...")
                sleep(1000)
            else:
                return True
        return False

    def online(self):
        if self.th is None:
            return False
        if not self.flag_first_connect:
            return False
        if self.mqtt.pending_subscriptions()!=0:
            return False
        if not self.mqtt.is_connected():
            return False
        if not self.has_time():
            # Resend config if enough time is passed from last.
            # Time delta can be negative because of positive clock skew
            # (clock in the future) can happen on soft resets.
            if (abs(time.now()-self.flag_last_config))>15:
                zdebug("resending config...")
                self.flag_last_config=time.now()
                self._config()
            return False
        return True

    def has_time(self):
        return self.flag_has_time

    def connected(self):
        return self.mqtt.is_connected() and self.mqtt.pending_subscriptions()==0


    def publish(self, payload, tag="default", timeout=0):
        if type(payload) is not PDICT:
            raise TypeError("Payload must be a dictionary")
        topic = self.data_topic
        topic += '/' + tag
        self.update_clock()
        self._mqtt_publish(topic, payload, timeout)

    def upload(self, path, remote_name, timeout=0):
        fd = fs.open(path, 'r')
        zdebug("Uploading file, size:", path, fd.size())
        c=None
        resp=None
        url="https://"+self._cfg.upload_host+"/v3/upload"
        try:
            c = http.HTTP(timeout=timeout, ctx=self.ssl_ctx)
            zdebug("file, remote_name, url:", path, remote_name, url)
            resp = c.upload(url, fd, remote_name)
            zdebug("upload status:", resp.status)
        except Exception as e:
            if c is not None:
                c.destroy()
            fd.close()
            raise e
        if c is not None:
            c.destroy()
        fd.close()
        return resp.status if resp is not None else 400

    def reset(self, reason=ZDM_RESET_REASON_UNKNOWN):
        zinfo("resetting with reason:", reason)
        if self._reset_callback is not None:
            try:
                # Should the callback not return, reset still goes ahead
                th=thread(self._reset_callback, reason)
                # thread.join() unimplemented yet
                #th.join(3000)
            except Exception as e:
                zinfo("on_reset callback failed:", e)

        try:
            self.mqtt.disconnect()
        except Exception as e:
            zdebug("Error while disconnecting mqtt...", e)

        try:
            net.disconnect(0)
        except Exception as e:
            zdebug("Error while disconnecting interface...", e)

        try:
            net.down(0)
        except Exception as e:
            zdebug("Error while interface shutdown...", e)
        sleep(10000)
        mcu.reset()

    def request_status(self):
        self._request_delta('status', {})

    def request_time(self):
        zinfo("requesting time...")
        self._request_delta('now', {})
        return 0

    def request_zfs(self, v=""):
        self._request_delta('zfs_info', {"version":v})

# PRIVATE

    def _periodic_callbacks(self):
        zdebug("callback timer ticked")
        if not self.mqtt.is_connected():
            return
        now = time.now()
        if self._stats_source and (now-self._last_stats_sent>self._send_stats_every):
            self._send_stats()
        # GPS fix can temporary disconnect GSM on some HW module.
        # Getting cell info before doing the GPS fix to avoid transitioning "not connected" cell info.
        if self._cellular_source and not self.fota_ongoing and (now-self._last_cellular_sent>self._send_cellular_every):
            self._send_cellular()
        if self._gps_source and not self.fota_ongoing and (now-self._last_gps_sent>self._send_gps_every):
            self._send_gps()


    def _config(self):
        # enable incoming messages callback and request status
        zdebug("configuring client...")
        try:
            self.request_status()
            self._send_manifest()
            self._send_os_info()
        except Exception as e:
            zerror("configuration error", e)
            raise e


    def _handle_dn_msg(self, client, topic, data):
        try:
            zinfo("received message", data)
            payload = json.loads(data)
            if 'key' in payload:
                if payload['key'].startswith('@'):
                    self._handle_job_request(payload['key'][1:], payload['value'])
                elif payload['key'].startswith('#'):
                    self._handle_delta_request(payload['key'][1:], payload['value'])
                else:
                    zwarn("unknown dn message", payload["key"])

                if payload['key'] == '@reset':
                    self.reset(ZDM_RESET_REASON_JOB)
                if payload['key'] == "#status":
                    self.flag_has_time = True
                    ts = payload.get("version",0)//1000
                    self.update_clock(ts)
                    if self._time_callback is not None:
                        self._time_callback()
                elif payload['key'] == "#now":
                    ts = payload.get("value",{}).get("s",0)
                    self.update_clock(ts)
                    if self._time_callback is not None:
                        self._time_callback()
            else:
                zwarn("incorrect dn message format")
        except Exception as e:
            zerror(e)

    def update_clock(self, ts=0):
        if ts:
            zinfo("Sync time from ts:",ts)
            time.set(ts)
            return
        if self._set_clock > 0 and time.last_sync() > self._set_clock:
            try:
                ts = self._clock_source()
            except Exception as e:
                zerror("Clock source failed with",e)
                ts=0
            if ts:
                zinfo("Sync time from source:",ts)
                time.set(ts)
            else:
                time.set(time.now())


    def _handle_job_request(self, job, arg):
        if job == 'fota':
            self._handle_fota_job(arg)
        elif job == 'zfs':
            self._handle_zfs_job(arg)
        elif job in self.jobs:
            try:
                res = self.jobs[job](self, arg['args'])
            except Exception as e:
                zerror(e)
                res = 'exception '+str(e),
            self._reply_job(job, res)
        else:
            zwarn("invalid job request", job)
            self._reply_job(job, 'unsupported '+job)

    def _send_fota_response(self, ok, version="", msg=""):
        response = {
            "fw_version": version if version else zfota.current_version(),
            "result": "success" if ok else "fail",
            "msg": msg
        }
        if self._fota_callback:
            msg = self._fota_callback(self, response["result"], response)
            if msg:
                response["msg"]=msg
        self._reply_job('fota', response)

    def _send_zfs_response(self, ok, version="", msg=""):
        response = {
            "version": version if version else zfsm.current_version(),
            "result": "success" if ok else "fail",
            "msg": msg
        }
        if self._zfs_callback:
            msg = self._zfs_callback(self, response["result"], response)
            if msg:
                response["msg"]=msg
        self._reply_job('zfs', response)

    def _validate_dict_key(self, info, key):
        try:
            info[key]
            zdebug("Key found:",key)
        except Exception as e:
            zwarn("Missing key:",key,e)
            raise e

    def _validate_fota_info(self, info):
        zdebug("Validating FOTA info:",info)
        try:
            self._validate_dict_key(info, "fw_version")
            if info.get("fw_sources",None):
                self._validate_dict_key(info, "fw_sources")
                self._validate_dict_key(info["fw_sources"][0], "size")
                self._validate_dict_key(info["fw_sources"][1], "size")
                self._validate_dict_key(info["fw_sources"][0], "crc")
                self._validate_dict_key(info["fw_sources"][1], "crc")
                if  type(info["fw_sources"][0]["size"]) != PSMALLINT and \
                    type(info["fw_sources"][0]["size"]) != PINTEGER  and \
                    type(info["fw_sources"][1]["size"]) != PSMALLINT and \
                    type(info["fw_sources"][1]["size"]) != PINTEGER:
                    raise TypeError("Size not an int")
            else:
                zdebug("No fw_sources, skipping...")
        except Exception as e:
            zerror("Malformed fota info:",e)
            raise e

    def _handle_fota_job(self, arg):
        zinfo("handling fota job...")
        try:
            self._validate_fota_info(arg)
        except Exception as e:
            self._send_fota_response(False,msg="Malformed FOTA info")
            return

        zfota.summary()
        if not self.permanent_fota:
            # not permanent mode, so we are in testing mode
            # if we are here, we are connected and able to receive from ZDM
            # accept fota.
            if self._fota_callback:
                zinfo("calling fota callback to accept fota")
                msg = self._fota_callback(self, "accept",arg["fw_version"])
                if msg:
                    zinfo("not accepted!",msg)
                    zfota.fail()
                    self._send_fota_response(False,msg=msg)
                    sleep(2000)
                    self.fota_ongoing = False
                    self.reset(ZDM_RESET_REASON_FOTA)
                    return

            zinfo("fota ok, finalizing")
            zfota.finalize()
            self._send_fota_response(True)
            self._send_os_info()
            self.permanent_fota = True
            return

        if zfsm.ongoing:
            zinfo("Abort FOTA during ZFS")
            self._send_fota_response(False,version=arg["fw_version"],msg="Not during ZFS")
            return

        if self.fota_ongoing:
            zinfo("Another FOTA is ongoing...")
            self._send_fota_response(False,version=arg["fw_version"],msg="Not during FOTA")
            return

        if zfota.current_version() == arg["fw_version"]:
            zinfo("fota to same version, skip")
            self._send_fota_response(True,version=arg["fw_version"])
            return

        # check if version is ok
        if self._fota_callback:
            msg = self._fota_callback(self, "check_version",arg['fw_version'])
            if msg:
                zwarn("fota aborted by callback", msg)
                self._send_fota_response(False,version=arg["fw_version"],msg=msg)
                zfota.cleanup()
                return

        # ok, request more info
        self._request_delta('fota_info', {"fw_version":arg["fw_version"]})

    def _handle_zfs_job(self, arg):
        zinfo("handling zfs job...")
        if not self.permanent_fota:
            zinfo("not handling zfs job while in testing mode...")
            self._send_zfs_response(False,msg="Not during FOTA")
            return

        if zfsm.ongoing:
            zinfo("zfs is ongoing...")
            self._send_zfs_response(False,msg="Not during ZFS")
            return

        if zfota.ongoing:
            zinfo("fota is ongoing...")
            self._send_zfs_response(False,msg="Not during FOTA")
            return

        if self._zfs_callback:
            zinfo("calling zfs callback for acceptance")
            msg = self._zfs_callback(self, "accept",arg["version"])
            if msg:
                zinfo("not accepted!",msg)
                self._send_zfs_response(False,msg=msg)
                return

        if zfsm.current_version() == arg["version"]:
            zinfo("zfs to same version, skip")
            self._send_zfs_response(True,version=arg["version"])
            return

        # check if version is ok
        if self._zfs_callback:
            msg = self._zfs_callback(self, "check_version",arg['version'])
            if msg:
                zwarn("zfs aborted by callback", msg)
                self._send_zfs_response(False,version=arg["version"],msg=msg)
                return

        # ok, request more info
        self.request_zfs(arg["version"])

    def _handle_delta_request(self, delta_key, arg):
        zinfo("delta request with key", delta_key)
        if delta_key == 'status':
            self._handle_delta_status(arg)
        elif delta_key == 'fota_info':
            self._handle_fota_info(arg)
        elif delta_key == 'zfs_info':
            self._handle_zfs_info(arg)
        # elif delta_key == 'now':
        #     self._handle_delta_timestamp(arg)
        else:
            zwarn("unknown custom delta")


    def _handle_delta_status(self, arg):
        zdebug("received status delta", arg)
        if not self.permanent_fota:
            # we are in testing mode
            # and we received a #status response
            # if there is no @fota, we are in trouble
            if ("expected" not in arg) or (arg["expected"] is None) or ("@fota" not in arg["expected"]):
                # there is no @fota!
                zinfo("Testing firmware and not @fota...revert immediately")
                self.reset(ZDM_RESET_REASON_FOTA_REVERT)
        if ('expected' in arg) and (arg['expected'] is not None):
            # handle other keys
            for expected_key in arg['expected']:
                value = arg['expected'][expected_key]['v']

                if expected_key[0] == '@':
                    self._handle_job_request(expected_key[1:], value)
                else:
                    self.expected.update({expected_key: value})

        if ('current' in arg) and (arg['current'] is not None):
            for current_key in arg['current']:
                if current_key[0] == '_':
                    pass
                else:
                    self.current.update({current_key: arg['current'][current_key]['v']})

    def _handle_fota_info(self, arg):
        zinfo("Handling fota_info")

        try:
            self._validate_fota_info(arg)
        except Exception as e:
            self._send_fota_response(False,msg="Malformed FOTA info")
            return

        if zfsm.ongoing:
            zinfo("Abort FOTA during ZFS")
            self._send_fota_response(False,version=arg["fw_version"],msg="Not during ZFS")
            return

        if self.fota_ongoing:
            zinfo("Another FOTA is ongoing...")
            self._send_fota_response(False,version=arg["fw_version"],msg="Not during FOTA")
            return

        try:
            self.fota_ongoing = True
            zfota.start(arg,self.ssl_ctx, self)
            zfota.ongoing=False
        except Exception as e:
            self._send_fota_response(False,version=arg["fw_version"],msg=str(e))
            zfota.cleanup()
            self.fota_ongoing = False
            return

        sleep(1000)
        zinfo("fota handled, resetting...")
        self.fota_ongoing = False
        self.reset(ZDM_RESET_REASON_FOTA)

    def _handle_zfs_info(self, arg):
        zinfo("Handling zfs_info")

        if zfsm.ongoing:
            zinfo("Another ZFS is ongoing...")
            self._send_zfs_response(False,version=arg["version"],msg="Not during ZFS")
            return

        if zfota.ongoing:
            zinfo("Abort ZFS during FOTA")
            self._send_zfs_response(False,version=arg["version"],msg="Not during FOTA")
            return

        try:
            msg = zfsm.start(arg,self.ssl_ctx, self)
        except Exception as e:
            self._send_zfs_response(False,version=arg["version"],msg=str(e))
            zfsm.ongoing=False
            return

        if msg:
            self._send_zfs_response(False,version=arg["version"],msg=msg)
            zfsm.ongoing=False
            return


        sleep(1000)
        zinfo("zfs handled, resetting...")
        self._send_zfs_response(True,version=arg["version"])
        self.reset(ZDM_RESET_REASON_ZFS)

    def _update_status_key(self, key, value):
        # update key:value on zdm and on self.current
        self._send_up_msg('', key, value)

        if key[0] != '_':
            self.current[key] = value

    def _clear_status_key(self, key):
        # remove status key from zdm and self.current
        self._send_up_msg('', key, None)
        self.current.pop(key, None)

    def _request_delta(self, key, value):
        self._send_up_msg('#', key, value)

    def _reply_job(self, key, value):
        self._send_up_msg('@', key, value)

    def _mqtt_publish(self, topic, payload, timeout=0):
        payload = json.dumps(payload)
        self.mqtt.publish(topic, payload, qos=self._cfg.qos_publish, retain=False, timeout=timeout)

    def _send_up_msg(self, prefix, key, value):
        msg = {
            'key': prefix + key,
            'value': value
        }
        self._mqtt_publish(self.up_topic, msg)
        zdebug("sent up msg with key", prefix+key, msg)

    def _send_manifest(self):
        value = {
            'jobs': [k for k in self.jobs],
        }
        self._update_status_key("__manifest", value)

    def _send_os_info(self):
        value = {
            "target": ZERYNTH_TARGET,
            "fw": zfota.current_version(),
            "zfs": zfsm.current_version(),
            "boot": zfota.bootloader(),
        #:if ZERYNTH_TEMPLATE_SOLUTION
            "template": ZERYNTH_TEMPLATE_NAME,
            "template_version": ZERYNTH_TEMPLATE_VERSION,
        #:endif
            "os": ZERYNTH_SDK_VERSION
        }
        self._update_status_key("__info", value)

    def _send_stats(self):
        try:
            zinfo("gathering stats...")
            res = self._stats_source(self)
            self._update_status_key("__stats", res)
            self._last_stats_sent = time.now()
        except Exception as e:
            zerror("stats callback failed with",e)

    def _send_gps(self):
        try:
            zinfo("gathering gnss info...")
            self._gps_source.start()
            res = self._gps_source.fix()
            self._update_status_key("__gnss", {
                "lat":res[0],
                "lon":res[1],
                "altitude":res[3],
                "speed":res[6]})
            self._last_gps_sent = time.now()
        except Exception as e:
            zerror("gps callback failed with",e)


    def _send_cellular(self):
        try:
            zinfo("gathering cellular info...")
            nfo = self._cellular_source.cellinfo()
            if nfo[0] in ("NOCONN","CONNECT"):
                rssi = self._cellular_source.rssi()
                self._update_status_key("__cellular", {
                    "operator":nfo[10],
                    "rssi":rssi,
                    "mcc":nfo[2][0:3],
                    "mcn":nfo[2][3:],
                    "lac":nfo[5],
                    "cid":nfo[6],
                    "network":nfo[1]})
                self._last_cellular_sent = time.now()
        except Exception as e:
            zerror("cellular callback failed with",e)

    def get_fota_percentages(self):
        self.fota_percentage = zfota.get_percentages()
        return self.fota_percentage

    def get_fota_byterate(self):
        self.fota_brate = zfota.get_brate()
        return self.fota_brate
