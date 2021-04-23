import gpio
import can

# Can transmit
def can_transmit(exp_can, ch, tx_b, sid):
    try:
        exp_can.transmit(ch, tx_b, sid)
    except PeripheralError:
        print("Can TX failed")

# Send a PING and wait for a PONG with CAN
def ping_starter(exp_can, tx, rx):
    # The chosed ID will pass the filter
    sid = 0x300
    while True:
        print("Sending PING")
        tx_buf = bytearray("PING")
        can_transmit(exp_can, tx, tx_buf, sid)
        sleep(500)
        # Check if we received a message on alert pin
        if gpio.get(INTR) is 0:
            rx_buf = exp_can.receive(rx, 4)
            if str(rx_buf[1]) == "PONG":
                print("PING-PONG done\n")
            else:
                print("PING-PONG failed\n")
        sleep(2000)

# Wait for a PING and answer with a PONG on CAN
def ping_receiver(exp_can, tx, rx):
    # The chosed ID will pass the filter
    sid = 0x300
    while True:
        # Check if we received a message on alert pin
        if gpio.get(INTR) is 0:
            rx_buf = exp_can.receive(rx, 4)
            print(rx_buf)
            if str(rx_buf[1]) == "PING":
                print("Sending PONG")
                tx_buf = bytearray("PONG")
                can_transmit(exp_can, tx, tx_buf, sid)