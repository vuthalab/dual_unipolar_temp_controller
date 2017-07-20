from PyQt4 import QtGui, QtCore, uic
from pyqtgraph.dockarea import DockArea, Dock
import os
from widgets.BlankWidget import BlankWidget


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

    def setupUi(self):
        pass

    def createDocks(self):
        self.blank_widget = BlankWidget(self.settings, self)
        self.blank_widget_dock = Dock('Blank Widget',
                                        widget=self.blank_widget)
        self.dock_area.addDock(self.blank_widget_dock)

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
        self.blank_widget.saveSettings()
        self.saveSettings()
