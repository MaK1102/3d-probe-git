import serial
import time

arduino = serial.Serial(port='COM4',   baudrate=9600, timeout=.1)


def write_read():
    data = arduino.readline()
    return   data


while True:
    value   = write_read()
    print(value)
