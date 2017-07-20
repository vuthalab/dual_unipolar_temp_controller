import serial
import struct
import time

"""

struct Params {
  unsigned int enable0;
  unsigned int set_temp0;
  float prop_gain0;
  float pi_pole0;
  float pd_pole0;

  unsigned int enable1;
  unsigned int set_temp1;
  float prop_gain1;
  float pi_pole1;
  float pd_pole1;

};


struct Logger {
  unsigned int act_temp0;
  unsigned int act_temp1;

  unsigned int gate_voltage0;
  unsigned int gate_voltage1;

  int error_signal0;
  int error_signal1;

};

"""

params_struct_size = 2*4 + 4*6
params_struct_fmt = '<HHfffHHfff'

logger_struct_size = 2*6
logger_struct_fmt = '<HHHHhh'


class DualUnipolarTemperatureController:

    def __init__(self, serialport='COM15'):
        self.serialport = serialport
        self.ser = serial.Serial(serialport, baudrate=115200)

    def idn(self):
        self.ser.write(b'i')
        return self.ser.readline()

    def get_params(self, get_read_write_string=False):
        write_string = b'g'
        self.ser.write(write_string)
        data = self.ser.read(self.params_struct_size)
        data_tuple = struct.unpack(self.params_struct_fmt, data)
        if get_read_write_string:
            return data_tuple, write_string, data
        else:
            return data_tuple

    def get_logger(self, get_read_write_string=False):
        write_string = b'l'
        self.ser.write(write_string)
        data = self.ser.read(self.logger_struct_fmt)
        data_tuple = struct.unpack(self.logger_struct_fmt, data)
        if get_read_write_string:
            return data_tuple, write_string, data
        else:
            return data_tuple

    def set(self, data_tuple):
        self.ser.write(b's')
        data = struct.pack(self.struct_fmt, *data_tuple)
        self.ser.write(data)

    def close(self):
        self.ser.close()


if __name__ == '__main__':
    dutc = DualUnipolarTemperatureController()
