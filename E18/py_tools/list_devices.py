#!/usr/bin/python3

# E18 c2530 chip serial port
# Bus 001 Device 004: ID 1a86:7523 QinHeng Electronics HL-340 USB-Serial adapter
# Bus 001 Device 003: ID 1a86:7523 QinHeng Electronics HL-340 USB-Serial adapter
#       idVendor           0x1a86 QinHeng Electronics
#       idProduct          0x7523 HL-340 USB-Serial adapter


import serial
import serial.tools.list_ports

DEV_TYPE = {0: "COORDINATOR",
            1: "ROUTER",
            2: "TERMINAL"
            }

NWK_STATE = {0: "NO NETWORK",
             1: "NETWORK EXISTS"}

BAUDRATE = 115200
TIMEOUT = 1
VID = 0x1a86  # 6790
PID = 0x7523  # 29987
VENDOR = "QinHeng Electronics"
PRODUCT = "HL-340 USB-Serial adapter"
e18_devices = []

serialPortList = serial.tools.list_ports.comports()
for serialPort in serialPortList:
    if serialPort.vid == VID and serialPort.pid == PID:
        print('Found ' + serialPort.device + ' as an Ebyte E18 device ')
        print("device : {}".format(serialPort.device))
        print("name : {}".format(serialPort.name))
        print("description : {}".format(serialPort.description))
        print("hwid : {}".format(serialPort.hwid))
        print("vid : {}".format(serialPort.vid))
        print("pid : {}".format(serialPort.pid))
        print("serial_number : {}".format(serialPort.serial_number))
        print("location : {}".format(serialPort.location))
        print("manufacturer : {}".format(serialPort.manufacturer))
        print("product : {}".format(serialPort.product))
        print("interface : {} \n".format(serialPort.interface))
        e18_devices.append(serialPort)

for dev in e18_devices:
    print("Open Serial connection to : {}".format(dev.device))
    ser = serial.Serial(dev.device)
    ser.baudrate = BAUDRATE
    ser.timeout = TIMEOUT
    txBytes = b"\xfe\x01\xfe\xff"
    print("Tx : {}".format(txBytes))
    ser.write(txBytes)
    rxBytes = ser.read(46)
    rxByteArray = bytearray(rxBytes)
    print("Rx : {}".format(rxBytes))
    print("Device Type   : {}".format(DEV_TYPE[rxByteArray[0]]))
    print("Network State : {}".format(NWK_STATE[rxByteArray[1]]))
    print("Network PANID : {:X}{:X}".format(rxByteArray[2], rxByteArray[3]))
    print("Network KEY   : {:X}{:X}{:X}{:X}{:X}{:X}{:X}{:X}{:X}{:X}{:X}{:X}{:X}{:X}{:X}{:X} ".format(rxByteArray[4],
                                                                                                     rxByteArray[5],
                                                                                                     rxByteArray[6],
                                                                                                     rxByteArray[7],
                                                                                                     rxByteArray[8],
                                                                                                     rxByteArray[9],
                                                                                                     rxByteArray[10],
                                                                                                     rxByteArray[11],
                                                                                                     rxByteArray[12],
                                                                                                     rxByteArray[13],
                                                                                                     rxByteArray[14],
                                                                                                     rxByteArray[15],
                                                                                                     rxByteArray[16],
                                                                                                     rxByteArray[17],
                                                                                                     rxByteArray[18],
                                                                                                     rxByteArray[19],
                                                                                                     rxByteArray[20],
                                                                                                     ))
    print("Network ShortAddr : {:X}{:X}".format(rxByteArray[21], rxByteArray[22]))

    print("Close Serial connection to : {}".format(dev.device))
    ser.close()
