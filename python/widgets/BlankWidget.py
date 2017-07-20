from PyQt4 import QtGui, QtCore, uic
import os


class BlankWidget(QtGui.QWidget):

    def __init__(self, settings, parent=None):
        super(BlankWidget, self).__init__(parent)
        self.settings = settings
        self.setupUi()
        self.loadSettings()

    def setupUi(self):
        pass

    def loadSettings(self):
        self.settings.beginGroup('blankwidget')
        self.settings.endGroup()

    def saveSettings(self):
        self.settings.beginGroup('blankwidget')
        self.settings.endGroup()

