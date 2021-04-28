
from zsensors import sensor

sens_dict = {}
sensors_name = []
to_send = {}

def init_sensors():
    global sens_dict
    sens_dict = sensor.get_sensors_dict()
    sensors_name = [e for e in sens_dict.keys()]
    print("Configured sensors: ", sensors_name)

def read_analog():
    for key, sens in sens_dict.items():
        sens.read()


def print_values():
    # Print values
    for key, sens in sens_dict.items():
        print(" - ", key, "     :", sens.get_value())

def data_to_send():
    global to_send
    for key, sens in sens_dict.items():
        to_send[key] = sens.get_value()
    return to_send
