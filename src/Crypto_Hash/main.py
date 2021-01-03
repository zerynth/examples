################################################################################
# Secure Hash
#
# Created by Zerynth Team 2017 CC
# Authors: G.Baldi
################################################################################

import streams

# import all supported hash functions
from crypto.hash import md5 as md5
from crypto.hash import sha1 as sha1
from crypto.hash import sha2 as sha2
from crypto.hash import sha3 as sha3
from crypto.hash import keccak as keccak
# also import HMAC
from crypto.hash import hmac as hmac

# open stdout
streams.serial()

message = "Zerynth"

while True:
    try:
        ss = md5.MD5()
        ss.update(message)
        print("MD5: ",ss.hexdigest())

        ss = sha1.SHA1()
        ss.update(message)
        print("SHA1:",ss.hexdigest())
        
        ss = sha2.SHA2(sha2.SHA512)
        ss.update(message)
        print("SHA2:",ss.hexdigest())
        
        ss = sha3.SHA3()
        ss.update(message)
        print("SHA3:",ss.hexdigest())

        ss = keccak.Keccak()
        ss.update(message)
        print("KECCAK:",ss.hexdigest())

        # generate a hmac with key="Python" and sha1 hash
        hh = hmac.HMAC("Python",sha1.SHA1())
        hh.update(message)
        print("HMAC:",hh.hexdigest())
    except Exception as e:
        print(e)
    sleep(2000)
