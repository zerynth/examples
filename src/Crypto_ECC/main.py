################################################################################
# Elliptic Curve Cryptography
#
# Created by Zerynth Team 2017 CC
# Authors: G. Baldi
################################################################################

import streams

# import ecc and sha1 modules
from crypto.ecc import ecc as ec
from crypto.hash import sha1 as sha1

streams.serial()

message = "Zerynth"

# import a Public Key for SECP256R1
pb = ec.hex_to_bin("7A181C7D3AD54EC3817CBAF86EA4E003AD492D8569102392A6EFE0C27E471A65553918EA1BAC86A68C78A30E9FE725EA499E14BEA96C3FE85E2267B74385E56B")
# import a Private Key for SECP256R1
pv = ec.hex_to_bin("6D5BE10E67D479FF99421A8DE030E2B4C5323EE477DA4C17420936CAC49C261E")

while True:
    # calculate hash of message
    ss = sha1.SHA1()
    ss.update(message)
    digest = ss.digest()

    # Calculate non deterministic signature of digest
    # for SECP256R1 and pv
    signature = ec.sign(ec.SECP256R1,digest,pv)
    
    # Calculate the deterministic signature of digest using SHA1
    deterministic_signature = ec.sign(ec.SECP256R1,digest,pv,deterministic=sha1.SHA1())

    print("PVKEY:",ec.bin_to_hex(pv))
    print("PBKEY:",ec.bin_to_hex(pb))
    # this changes each loop because of random number generator
    print("SIGNED:",ec.bin_to_hex(signature))
    # this is always the same
    print("SIGNED (det)",ec.bin_to_hex(deterministic_signature))

    print("VERIFY SIGNATURE:", ec.verify(ec.SECP256R1,digest,signature,pb))
    print("VERIFY SIGNATURE (det):", ec.verify(ec.SECP256R1,digest,deterministic_signature,pb))
    # tampered digests are detected
    print("VERIFY TAMPERED:", ec.verify(ec.SECP256R1,digest+b'\x00',signature,pb))
    print("-"*20)
    sleep(2000)
