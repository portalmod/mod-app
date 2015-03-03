#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# MOD-App
# Copyright (C) 2014-2015 Filipe Coelho <falktx@falktx.com>
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License as
# published by the Free Software Foundation; either version 3 of
# the License, or any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# For a full copy of the GNU General Public License see the LICENSE file.

# ------------------------------------------------------------------------------------------------------------
# Imports (Custom)

from mod_common import *

# ------------------------------------------------------------------------------------------------------------
# Imports (Global)

if config_UseQt5:
    from PyQt5.QtCore import pyqtSlot
    from PyQt5.QtGui import QFontMetrics, QIcon
    from PyQt5.QtWidgets import QDialog, QDialogButtonBox, QFileDialog, QMessageBox
else:
    from PyQt4.QtCore import pyqtSlot
    from PyQt4.QtGui import QDialog, QDialogButtonBox, QFileDialog, QFontMetrics, QIcon, QMessageBox

# ------------------------------------------------------------------------------------------------------------
# Imports (UI)

from ui_mod_settings import Ui_SettingsWindow

# ------------------------------------------------------------------------------------------------------------
# Settings Dialog

class SettingsWindow(QDialog):
    # Tab indexes
    TAB_INDEX_MAIN    = 0
    TAB_INDEX_HOST    = 1
    TAB_INDEX_WEBVIEW = 2

    # --------------------------------------------------------------------------------------------------------

    def __init__(self, parent=None):
        QDialog.__init__(self, parent)
        self.ui = Ui_SettingsWindow()
        self.ui.setupUi(self)

        # ----------------------------------------------------------------------------------------------------
        # Set up GUI

        self.ui.cb_host_jack_bufsize_value.lineEdit().setInputMask("9999")
        self.ui.lw_page.setFixedWidth(48 + 6*4 + QFontMetrics(self.ui.lw_page.font()).width("  WebView  "))

        # Not possible with ingen right now
        self.ui.cb_host_verbose.setEnabled(False)

        # ----------------------------------------------------------------------------------------------------
        # Load Settings

        self.loadSettings()

        # ----------------------------------------------------------------------------------------------------
        # Set-up connections

        self.accepted.connect(self.slot_saveSettings)
        self.ui.buttonBox.button(QDialogButtonBox.Reset).clicked.connect(self.slot_resetSettings)

        self.ui.tb_main_proj_folder_open.clicked.connect(self.slot_getAndSetProjectPath)
        self.ui.tb_host_path.clicked.connect(self.slot_getAndSetModHostPath)

        # ----------------------------------------------------------------------------------------------------
        # Post-connect setup

        self.ui.lw_page.setCurrentCell(0, 0)

    # --------------------------------------------------------------------------------------------------------

    def loadSettings(self):
        settings = QSettings()

        # ----------------------------------------------------------------------------------------------------
        # Main

        self.ui.le_main_proj_folder.setText(settings.value(MOD_KEY_MAIN_PROJECT_FOLDER, MOD_DEFAULT_MAIN_PROJECT_FOLDER, type=str))
        self.ui.sb_main_refresh_interval.setValue(settings.value(MOD_KEY_MAIN_REFRESH_INTERVAL, MOD_DEFAULT_MAIN_REFRESH_INTERVAL, type=int))

        # ----------------------------------------------------------------------------------------------------
        # Host

        self.ui.cb_host_jack_bufsize_change.setChecked(settings.value(MOD_KEY_HOST_JACK_BUFSIZE_CHANGE, MOD_DEFAULT_HOST_JACK_BUFSIZE_CHANGE, type=bool))
        self.ui.cb_host_verbose.setChecked(settings.value(MOD_KEY_HOST_VERBOSE, MOD_DEFAULT_HOST_VERBOSE, type=bool))

        hostPath = settings.value(MOD_KEY_HOST_PATH, MOD_DEFAULT_HOST_PATH, type=str)
        if hostPath.endswith("mod-host"):
            hostPath = MOD_DEFAULT_HOST_PATH
        self.ui.le_host_path.setText(hostPath)

        availableBufSizes = [int(self.ui.cb_host_jack_bufsize_value.itemText(i)) for i in range(self.ui.cb_host_jack_bufsize_value.count())]
        currentBufSize    = settings.value(MOD_KEY_HOST_JACK_BUFSIZE_VALUE, MOD_DEFAULT_HOST_JACK_BUFSIZE_VALUE, type=int)

        if currentBufSize in availableBufSizes:
            self.ui.cb_host_jack_bufsize_value.setCurrentIndex(self.ui.cb_host_jack_bufsize_value.findText(str(currentBufSize)))
        else:
            self.ui.cb_host_jack_bufsize_value.addItem(str(currentBufSize))
            self.ui.cb_host_jack_bufsize_value.setCurrentIndex(len(availableBufSizes))

        # ----------------------------------------------------------------------------------------------------
        # WebView

        self.ui.cb_webview_inspector.setChecked(settings.value(MOD_KEY_WEBVIEW_INSPECTOR, MOD_DEFAULT_WEBVIEW_INSPECTOR, type=bool))
        self.ui.cb_webview_verbose.setChecked(settings.value(MOD_KEY_WEBVIEW_VERBOSE, MOD_DEFAULT_WEBVIEW_VERBOSE, type=bool))

    # --------------------------------------------------------------------------------------------------------

    @pyqtSlot()
    def slot_saveSettings(self):
        settings = QSettings()

        # ----------------------------------------------------------------------------------------------------
        # Main

        settings.setValue(MOD_KEY_MAIN_PROJECT_FOLDER,   self.ui.le_main_proj_folder.text())
        settings.setValue(MOD_KEY_MAIN_REFRESH_INTERVAL, self.ui.sb_main_refresh_interval.value())

        # ----------------------------------------------------------------------------------------------------
        # Host

        settings.setValue(MOD_KEY_HOST_JACK_BUFSIZE_CHANGE, self.ui.cb_host_jack_bufsize_change.isChecked())
        settings.setValue(MOD_KEY_HOST_JACK_BUFSIZE_VALUE,  int(self.ui.cb_host_jack_bufsize_value.currentText()))
        settings.setValue(MOD_KEY_HOST_VERBOSE,             self.ui.cb_host_verbose.isChecked())
        settings.setValue(MOD_KEY_HOST_PATH,                self.ui.le_host_path.text())

        # ----------------------------------------------------------------------------------------------------
        # WebView

        settings.setValue(MOD_KEY_WEBVIEW_INSPECTOR, self.ui.cb_webview_inspector.isChecked())
        settings.setValue(MOD_KEY_WEBVIEW_VERBOSE,   self.ui.cb_webview_verbose.isChecked())

    # --------------------------------------------------------------------------------------------------------

    @pyqtSlot()
    def slot_resetSettings(self):
        # ----------------------------------------------------------------------------------------------------
        # Main

        if self.ui.lw_page.currentRow() == self.TAB_INDEX_MAIN:
            self.ui.le_main_proj_folder.setText(MOD_DEFAULT_MAIN_PROJECT_FOLDER)
            self.ui.sb_main_refresh_interval.setValue(MOD_DEFAULT_MAIN_REFRESH_INTERVAL)

        # ----------------------------------------------------------------------------------------------------
        # Host

        elif self.ui.lw_page.currentRow() == self.TAB_INDEX_HOST:
            self.ui.cb_host_jack_bufsize_change.setChecked(MOD_DEFAULT_HOST_JACK_BUFSIZE_CHANGE)
            self.ui.cb_host_jack_bufsize_value.setCurrentIndex(self.ui.cb_host_jack_bufsize_value.findText(str(MOD_DEFAULT_HOST_JACK_BUFSIZE_VALUE)))
            self.ui.cb_host_verbose.setChecked(MOD_DEFAULT_HOST_VERBOSE)
            self.ui.le_host_path.setText(MOD_DEFAULT_HOST_PATH)

        # ----------------------------------------------------------------------------------------------------
        # WebView

        elif self.ui.lw_page.currentRow() == self.TAB_INDEX_WEBVIEW:
            self.ui.cb_webview_inspector.setChecked(MOD_DEFAULT_WEBVIEW_INSPECTOR)
            self.ui.cb_webview_verbose.setChecked(MOD_DEFAULT_WEBVIEW_VERBOSE)

    # --------------------------------------------------------------------------------------------------------

    @pyqtSlot()
    def slot_getAndSetProjectPath(self):
        newPath = QFileDialog.getExistingDirectory(self, self.tr("Set Default Project Path"), self.ui.le_main_proj_folder.text(), QFileDialog.ShowDirsOnly)
        if not newPath:
            return

        self.ui.le_main_proj_folder.setText(newPath)

    @pyqtSlot()
    def slot_getAndSetModHostPath(self):
        newPath = QFileDialog.getExistingDirectory(self, self.tr("Set Path to mod-host"), self.ui.le_host_path.text())
        if not newPath:
            return

        if not os.path.isfile(newPath):
            return QMessageBox.critical(self, self.tr("Error"), "Path to mod-host must be a valid filename")

        self.ui.le_host_path.setText(newPath)

    # --------------------------------------------------------------------------------------------------------

    def done(self, r):
        QDialog.done(self, r)
        self.close()

# ------------------------------------------------------------------------------------------------------------
# Main (for testing Settings UI)

if __name__ == '__main__':
    # --------------------------------------------------------------------------------------------------------
    # App initialization

    if config_UseQt5:
        from PyQt5.QtWidgets import QApplication
    else:
        from PyQt4.QtGui import QApplication

    app = QApplication(sys.argv)
    app.setApplicationName("MOD-Settings")
    app.setApplicationVersion(config["version"])
    app.setOrganizationName("MOD")
    app.setWindowIcon(QIcon(":/48x48/mod.png"))

    # --------------------------------------------------------------------------------------------------------
    # Create GUI

    gui = SettingsWindow()

    # --------------------------------------------------------------------------------------------------------
    # Show GUI

    gui.show()

    # --------------------------------------------------------------------------------------------------------
    # App-Loop

    sys.exit(app.exec_())

# ------------------------------------------------------------------------------------------------------------
