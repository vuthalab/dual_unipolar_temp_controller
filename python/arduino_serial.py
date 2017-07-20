import serial
import struct
import time


class DualUnipolarTemperatureController:

    struct_size = 16  # bytes
    struct_fmt = '<HHHHHHhh'

    def __init__(self, serialport='COM15'):
        self.serialport = serialport
        self.ser = serial.Serial(serialport, baudrate=115200)

    def idn(self):
        self.ser.write(b'i')
        return self.ser.readline()

    def get(self):
        self.ser.write(b'g')
        data = self.ser.read(self.struct_size)
        data_tuple = struct.unpack(self.struct_fmt, data)
        return data_tuple

    def set(self, data_tuple):
        self.ser.write(b's')
        data = struct.pack(self.struct_fmt, *data_tuple)
        self.ser.write(data)


    def close(self):
        self.ser.close()


if __name__ == '__main__':
    dutc = DualUnipolarTemperatureController()
