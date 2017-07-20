from PyQt4 import QtGui, QtCore, uic
import os
from widgets.DictEditor import OrderedDictEditor
from collections import OrderedDict

default_data_dict = OrderedDict([
        ('Set Resistance 0 (kOhm):', 10.0),
        ('P gain 0:', 1.0),
        ('PI Pole 0 (Hz):', 2.0),
        ('PD Pole 0 (Hz):', 10.0),
        ('Servo Enable 0:', False),
        ('Set Resistance 1 (kOhm):', 10.0),
        ('P gain 1:', 1.0),
        ('PI Pole 1 (Hz):', 2.0),
        ('PD Pole 1 (Hz):', 10.),
        ('Servo Enable 1:', False)])


class DualTempCont(QtGui.QWidget):

    def __init__(self, settings, parent=None):
        super(DualTempCont, self).__init__(parent)
        self.settings = settings
        self.data_dict = OrderedDict(default_data_dict)
        self.setupUi()
        self.loadSettings()

    def setupUi(self):
        self.grid = QtGui.QGridLayout(self)

        self.data_editor = OrderedDictEditor(self.data_dict, self)
        self.grid.addWidget(self.data_editor, 0, 0, len(default_data_dict), 2)
        self.data_editor.valueChanged.connect(self.handleDictValueChanged)

        rowStart = len(default_data_dict)

        self.upload_button = QtGui.QPushButton('Upload', self)
        self.grid.addWidget(self.upload_button, rowStart, 0)

        self.download_button = QtGui.QPushButton('Download', self)
        self.grid.addWidget(self.download_button, rowStart, 1)

        self.load_from_eeprom_button = QtGui.QPushButton('Load from EEPROM', self)
        self.grid.addWidget(self.load_from_eeprom_button, rowStart + 1, 0)

        self.save_to_eeprom_button = QtGui.QPushButton('Save to EEPROM', self)
        self.grid.addWidget(self.save_to_eeprom_button, rowStart + 1, 1)

    def handleDictValueChanged(self):
        print(self.data_dict)

    def loadSettings(self):
        self.settings.beginGroup('DualTempCont')
        self.settings.endGroup()

    def saveSettings(self):
        self.settings.beginGroup('DualTempCont')
        self.settings.endGroup()

