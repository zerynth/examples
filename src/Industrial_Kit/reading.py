from bsp import board
import init.inputs as io
import mcu

def read_loop(agent):
    try:
        print("5 - ADC config...")
        #Create a dictionary with all FourZeroBox sensors
        io.init_sensors()
        print("... done")
    except Exception as e:
        print(e)
        mcu.reset()

    # Command string
    while True:
        try:
            sleep(10000)

            print("======== reading")
            # Analog sensors
            io.read_analog()
            io.print_values()
            print("======== done")

            # Publish mgmt
            try:
                to_send = io.data_to_send()
                agent.publish({ "pow1": to_send["power"] }, "power")
                agent.publish({ "temp": to_send["temperature"] }, "env")
            except Exception as e:
                print('Publish exception: ', e)
        except Exception as e:
            print("Reading loop Error: ", e)
            board.error_cloud()
            mcu.reset()