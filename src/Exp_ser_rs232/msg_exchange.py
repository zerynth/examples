import serial

# Send a PING and wait for the PONG from the other board.
def ping_starter(ser):
    while True:
        print("Sending PING")
        ser.write("PING")
        msg = ser.read(4)
        print("got", msg)
        if msg == "PONG":
            print("PING-PONG done\n")
            sleep(500)
        else:
            print("PING-PONG failed\n")
            sleep(2000)

# Wait for a PING and answer with a PONG
def ping_receiver(ser):
    while True:
        msg = ser.read(4)
        if msg == "PING":
            print("Sending PONG")
            ser.write("PONG")