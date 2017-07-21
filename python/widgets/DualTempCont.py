from PyQt4 import QtGui, QtCore, uic
import os
from widgets.DictEditor import OrderedDictEditor
from collections import OrderedDict
from arduino_serial import DualUnipolarTemperatureController
import numpy as np

default_data_dict = OrderedDict([
        ('Servo Enable 0:', False),
        ('Set Resistance 0 (kOhm):', 10.0),
        ('P gain 0:', 1.0),
        ('PI Pole 0 (Hz):', 2.0),
        ('PD Pole 0 (Hz):', 10.0),
        ('Servo Enable 1:', False),
        ('Set Resistance 1 (kOhm):', 10.0),
        ('P gain 1:', 1.0),
        ('PI Pole 1 (Hz):', 2.0),
        ('PD Pole 1 (Hz):', 10.)])



default_logger_dict = OrderedDict([
        ('Gate Voltage 0 (V):', 0.0),
        ('Gate Voltage 1 (V):', 0.0),
        ('Error signal 0 (V):', 0.0),
        ('Error signal 1 (V):', 0.0),
        ('Accumulator 0 (V):', 0.0),
        ('Accumulator 1 (V):', 0.0),
        ('dt (s):', 0.0)])

ZEROV = 2**15


class DualTempCont(QtGui.QWidget):

    def __init__(self, settings, parent=None):
        super(DualTempCont, self).__init__(parent)
        self.settings = settings
        self.logger_dict = OrderedDict(default_logger_dict)

        self.loadSettings()
        self.setupUi()

        self.dutc = DualUnipolarTemperatureController('COM15')

        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self.updateLogs)
        self.n_timer_events = 0
        self.timer.start(200)

    def setupUi(self):
        self.grid = QtGui.QGridLayout(self)

        self.data_editor = OrderedDictEditor(self.data_dict, self)
        self.grid.addWidget(self.data_editor, 0, 0, len(default_data_dict), 2)
        self.data_editor.valueChanged.connect(self.handleDictValueChanged)

        rowStart = len(default_data_dict)

        self.upload_button = QtGui.QPushButton('Upload', self)
        self.upload_button.clicked.connect(self.handleUploadClicked)
        self.grid.addWidget(self.upload_button, rowStart, 0)

        self.download_button = QtGui.QPushButton('Download', self)
        self.download_button.clicked.connect(self.handleDownloadClicked)
        self.grid.addWidget(self.download_button, rowStart, 1)

        self.load_from_eeprom_button = QtGui.QPushButton('Load from EEPROM', self)
        self.load_from_eeprom_button.clicked.connect(self.handleLoadFromEepromClicked)
        self.grid.addWidget(self.load_from_eeprom_button, rowStart + 1, 0)

        self.save_to_eeprom_button = QtGui.QPushButton('Save to EEPROM', self)
        self.save_to_eeprom_button.clicked.connect(self.handleSaveToEepromClicked)
        self.grid.addWidget(self.save_to_eeprom_button, rowStart + 1, 1)

        self.data_logger = OrderedDictEditor(self.logger_dict, self)
        self.grid.addWidget(self.data_logger, rowStart + 2, 0, len(default_logger_dict), 2)

    def handleDictValueChanged(self):
        pass

    def updateLogs(self):
        self.n_timer_events += 1
        if self.n_timer_events > 20:
            out = self.dutc.get_logger(True)
            log_tuple = out[0]
            print(log_tuple)
            offset = np.array([1., 1., 0., 0.])
            voltages = list((np.array(log_tuple[:4], dtype=float)/ZEROV - offset)*5.0)
            logdata_list = list(voltages) + list(log_tuple[4:])

            for i, k in enumerate(self.logger_dict.iterkeys()):
                self.logger_dict[k] = logdata_list[i]

            self.data_logger.updateValues()

    def handleUploadClicked(self):
        value_tuple = self.data_dict.values()
        (enable0, set_r0, pgain0, pi_pole0, pd_pole0) = value_tuple[:5]
        (enable1, set_r1, pgain1, pi_pole1, pd_pole1) = value_tuple[5:]

        # set voltage dac value
        set_v_dac0 = int((set_r0 - 10.)/(set_r0 + 10.)*ZEROV + ZEROV)
        set_v_dac1 = int((set_r1 - 10.)/(set_r1 + 10.)*ZEROV + ZEROV)

        data_tuple = (int(enable0), set_v_dac0, pgain0, pi_pole0, pd_pole0,
            int(enable1), set_v_dac1, pgain1, pi_pole1, pd_pole1)

        print('upload', data_tuple)
        print(self.dutc.set_params(data_tuple, True))


    def handleDownloadClicked(self):
        out = self.dutc.get_params(True)

        data_tuple = out[0]
        print('download', data_tuple)

        set_v_dac0 = data_tuple[1]
        set_v_dac1 = data_tuple[6]

        v0 = float(set_v_dac0 - ZEROV)/ZEROV
        v1 = float(set_v_dac1 - ZEROV)/ZEROV

        set_r0 = (1.+v0)/(1-v0)*10
        set_r1 = (1.+v1)/(1-v1)*10

        data_list = list(data_tuple)
        data_list[0] = bool(data_tuple[0])
        data_list[1] = set_r0
        data_list[5] = bool(data_tuple[5])
        data_list[6] = set_r1

        for i, k in enumerate(self.data_dict.iterkeys()):
            self.data_dict[k] = data_list[i]

        self.data_editor.updateValues()

    def handleLoadFromEepromClicked(self):
        print('loadfromeeprom')

    def handleSaveToEepromClicked(self):
        print('savetoeeprom')

    def loadSettings(self):
        self.settings.beginGroup('DualTempCont')
        data_dict_string = str(self.settings.value('data_dict').toString())
        print(data_dict_string)
        if data_dict_string is not "":
            self.data_dict = eval(data_dict_string)
        else:
            self.data_dict = OrderedDict(default_data_dict)
        self.settings.endGroup()

    def saveSettings(self):
        self.settings.beginGroup('DualTempCont')
        self.settings.setValue('data_dict', repr(self.data_dict))
        self.settings.endGroup()

