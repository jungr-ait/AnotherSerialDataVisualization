import serial.tools.list_ports

# returns a list of common baudrate
def serial_common_baud_rate_list():
    return ["9600", "14400", "19200", "38400", "57600", "115200", "128000", "230400", "256000", "500000", "1000000"]


# returns a list of all available serial device on your computer
def serial_device_list():
    device_list = []
    for d in serial.tools.list_ports.comports():
        device_list.append(d.device)
    return device_list

################################### END #########################################