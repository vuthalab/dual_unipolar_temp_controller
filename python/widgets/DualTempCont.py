from PyQt4 import QtGui, QtCore, uic
import os
from widgets.DictEditor import OrderedDictEditor
from collections import OrderedDict

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

ZEROV = 2**15


class DualTempCont(QtGui.QWidget):

    def __init__(self, settings, parent=None):
        super(DualTempCont, self).__init__(parent)
        self.settings = settings
        self.loadSettings()
        self.setupUi()

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

    def handleDictValueChanged(self):
        pass

    def handleUploadClicked(self):
        value_tuple = self.data_dict.values()
        (set_r0, pgain0, pi_pole0, pd_pole0, enable0) = value_tuple[:5]
        (set_r1, pgain1, pi_pole1, pd_pole1, enable1) = value_tuple[5:]

        # set voltage dac value
        print(set_r0)
        print(set_r1)
        set_v_dac0 = int((set_r0 - 10.)/(set_r0 + 10.)*ZEROV + ZEROV)
        set_v_dac1 = int((set_r1 - 10.)/(set_r1 + 10.)*ZEROV + ZEROV)

        print(set_v_dac0)
        print(set_v_dac1)

    def handleDownloadClicked(self):
        print('download')

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

