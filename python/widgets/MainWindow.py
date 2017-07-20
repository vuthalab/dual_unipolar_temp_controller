from PyQt4 import QtGui, QtCore, uic
from pyqtgraph.dockarea import DockArea, Dock
import os
from widgets.DualTempCont import DualTempCont


class MainWindow(QtGui.QMainWindow):
    """The only window of the application."""

    def __init__(self, settings):
        super(MainWindow, self).__init__()
        self.settings = settings

        self.setupUi()

        self.dock_area = DockArea()
        self.setCentralWidget(self.dock_area)

        self.createDocks()

        self.loadSettings()
        self.setWindowTitle('Dual Temperature Controller')

    def setupUi(self):
        pass

    def createDocks(self):
        self.dual_temp_cont = DualTempCont(self.settings, self)
        self.dual_temp_cont_dock = Dock('Dual Temp. Cont.',
                                        widget=self.dual_temp_cont)
        self.dock_area.addDock(self.dual_temp_cont_dock)

    def loadSettings(self):
        """Load window state from self.settings"""

        self.settings.beginGroup('mainwindow')
        geometry = self.settings.value('geometry').toByteArray()
        state = self.settings.value('windowstate').toByteArray()
        dock_string = str(self.settings.value('dockstate').toString())
        if dock_string is not "":
            dock_state = eval(dock_string)
            self.dock_area.restoreState(dock_state)
        self.settings.endGroup()

        self.restoreGeometry(geometry)
        self.restoreState(state)

    def saveSettings(self):
        """Save window state to self.settings."""
        self.settings.beginGroup('mainwindow')
        self.settings.setValue('geometry', self.saveGeometry())
        self.settings.setValue('windowstate', self.saveState())
        dock_state = self.dock_area.saveState()
        # dock_state returned here is a python dictionary. Coundn't find a good
        # way to save dicts in QSettings, hence just using representation
        # of it.
        self.settings.setValue('dockstate', repr(dock_state))
        self.settings.endGroup()

    def closeEvent(self, event):
        self.dual_temp_cont.saveSettings()
        self.saveSettings()
