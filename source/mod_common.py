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
# Generate a random port number between 9000 and 18000

from random import random

_PORT = str(8998 + int(random()*9000))

# ------------------------------------------------------------------------------------------------------------
# Mod-App Configuration

config = {
    # Address used for the webserver
    "addr": "http://127.0.0.1:%s" % _PORT,
    # Port used for the webserver
    "port": _PORT,
    # MOD-App version
    "version": "0.0.1"
}

del _PORT

# ------------------------------------------------------------------------------------------------------------
# Imports (Global)

import os
import sys

from PyQt5.QtCore import QDir, QSettings

# ------------------------------------------------------------------------------------------------------------
# Check if using live ISO

USING_LIVE_ISO   = bool("--using-live-iso"   in sys.argv)
SKIP_INTEGRATION = bool("--skip-integration" in sys.argv)

if USING_LIVE_ISO:
    config["addr"] = "http://127.0.0.1:17891"
    config["port"] = "17891"

# ------------------------------------------------------------------------------------------------------------
# Set CWD

CWD = sys.path[0]

if not CWD:
    CWD = os.path.dirname(sys.argv[0])

# make it work with cxfreeze
if os.path.isfile(CWD):
    CWD = os.path.dirname(CWD)

# ------------------------------------------------------------------------------------------------------------
# Use custom modules if available

if os.path.exists(os.path.join(CWD, "modules", "mod-ui")):
    print("NOTE: Using custom mod-ui module")
    sys.path = [os.path.join(CWD, "modules", "mod-ui")] + sys.path
    usingCustomMODUI = True
else:
    usingCustomMODUI = False

# ------------------------------------------------------------------------------------------------------------
# Set Platform

if sys.platform == "darwin":
    LINUX   = False
    MACOS   = True
    WINDOWS = False
elif "linux" in sys.platform:
    LINUX   = True
    MACOS   = False
    WINDOWS = False
elif sys.platform in ("win32", "win64", "cygwin"):
    LINUX   = False
    MACOS   = False
    WINDOWS = True
else:
    LINUX   = False
    MACOS   = False
    WINDOWS = False

# ------------------------------------------------------------------------------------------------------------
# Set up environment for the webserver

if usingCustomMODUI:
    ROOT = os.path.join(CWD, "modules", "mod-ui")
else:
    ROOT = "/usr/share/mod"

DATA_DIR = os.path.expanduser("~/.local/share/mod-data/")

os.environ['MOD_DEV_HOST'] = "0"
os.environ['MOD_DEV_HMI']  = "1"
os.environ['MOD_DESKTOP']  = "1"
os.environ['MOD_LOG']      = "0"

os.environ['MOD_DATA_DIR']           = DATA_DIR
os.environ['MOD_KEY_PATH']           = os.path.join(DATA_DIR, "keys")
os.environ['MOD_CLOUD_PUB']          = os.path.join(ROOT, "keys", "cloud_key.pub")
os.environ['MOD_HTML_DIR']           = os.path.join(ROOT, "html")
os.environ['MOD_PLUGIN_LIBRARY_DIR'] = os.path.join(DATA_DIR, "lib")

os.environ['MOD_DEFAULT_JACK_BUFSIZE']  = "0"
os.environ['MOD_PHANTOM_BINARY']        = "/usr/bin/phantomjs"
os.environ['MOD_SCREENSHOT_JS']         = os.path.join(ROOT, "screenshot.js")
os.environ['MOD_DEVICE_WEBSERVER_PORT'] = config["port"]
os.environ['MOD_INGEN_SOCKET_URI']      = "unix:///tmp/mod-app-%s.sock" % config["port"]

DATA_DIR_EMPTY = not os.path.exists(DATA_DIR)

# ------------------------------------------------------------------------------------------------------------
# Settings keys

# Main
MOD_KEY_MAIN_MODGUI_SHOW_MODE    = "Main/ModGuiShowMode"    # int
MOD_KEY_MAIN_PROJECT_FOLDER      = "Main/ProjectFolder"     # str
MOD_KEY_MAIN_REFRESH_INTERVAL    = "Main/RefreshInterval"   # int

# Host
MOD_KEY_HOST_NUM_AUDIO_INS       = "Host/NumAudioIns"       # int
MOD_KEY_HOST_NUM_AUDIO_OUTS      = "Host/NumAudioOuts"      # int
MOD_KEY_HOST_NUM_MIDI_INS        = "Host/NumMidiIns"        # int
MOD_KEY_HOST_NUM_MIDI_OUTS       = "Host/NumMidiOuts"       # int
MOD_KEY_HOST_NUM_CV_INS          = "Host/NumCvIns"          # int
MOD_KEY_HOST_NUM_CV_OUTS         = "Host/NumCvOuts"         # int
MOD_KEY_HOST_AUTO_CONNNECT_INS   = "Host/AutoConnectIns"    # bool
MOD_KEY_HOST_AUTO_CONNNECT_OUTS  = "Host/AutoConnectOuts"   # bool
MOD_KEY_HOST_VERBOSE             = "Host/Verbose"           # bool
MOD_KEY_HOST_PATH                = "Host/Path"              # str

# WebView
MOD_KEY_WEBVIEW_INSPECTOR        = "WebView/Inspector"      # bool
MOD_KEY_WEBVIEW_VERBOSE          = "WebView/Verbose"        # bool
MOD_KEY_WEBVIEW_SHOW_INSPECTOR   = "WebView/ShowInspector"  # bool

# ------------------------------------------------------------------------------------------------------------
# Settings defaults

# Main
MOD_DEFAULT_MAIN_MODGUI_SHOW_MODE    = 1
MOD_DEFAULT_MAIN_REFRESH_INTERVAL    = 30
MOD_DEFAULT_MAIN_PROJECT_FOLDER      = QDir.toNativeSeparators(QDir.homePath())

# Host
MOD_DEFAULT_HOST_NUM_AUDIO_INS       = 2
MOD_DEFAULT_HOST_NUM_AUDIO_OUTS      = 2
MOD_DEFAULT_HOST_NUM_MIDI_INS        = 1
MOD_DEFAULT_HOST_NUM_MIDI_OUTS       = 1
MOD_DEFAULT_HOST_NUM_CV_INS          = 0
MOD_DEFAULT_HOST_NUM_CV_OUTS         = 0
MOD_DEFAULT_HOST_AUTO_CONNNECT_INS   = True
MOD_DEFAULT_HOST_AUTO_CONNNECT_OUTS  = True
MOD_DEFAULT_HOST_VERBOSE             = False
MOD_DEFAULT_HOST_PATH                = "/usr/bin/ingen"

# WebView
MOD_DEFAULT_WEBVIEW_INSPECTOR        = False
MOD_DEFAULT_WEBVIEW_VERBOSE          = False
MOD_DEFAULT_WEBVIEW_SHOW_INSPECTOR   = False

# ------------------------------------------------------------------------------------------------------------
# Set initial settings

def setInitialSettings():
    if USING_LIVE_ISO:
        modguiShowMode = 1
        webviewVerbose = False

    else:
        qsettings = QSettings("MOD", "MOD-App")

        modguiShowMode  = qsettings.value(MOD_KEY_MAIN_MODGUI_SHOW_MODE,    MOD_DEFAULT_MAIN_MODGUI_SHOW_MODE,    type=int)
        webviewVerbose  = qsettings.value(MOD_KEY_WEBVIEW_VERBOSE,          MOD_DEFAULT_WEBVIEW_VERBOSE,          type=bool)

        os.environ['MOD_INGEN_NUM_AUDIO_INS']  = str(qsettings.value(MOD_KEY_HOST_NUM_AUDIO_INS,  MOD_DEFAULT_HOST_NUM_AUDIO_INS,  type=int))
        os.environ['MOD_INGEN_NUM_AUDIO_OUTS'] = str(qsettings.value(MOD_KEY_HOST_NUM_AUDIO_OUTS, MOD_DEFAULT_HOST_NUM_AUDIO_OUTS, type=int))
        os.environ['MOD_INGEN_NUM_MIDI_INS']   = str(qsettings.value(MOD_KEY_HOST_NUM_MIDI_INS,   MOD_DEFAULT_HOST_NUM_MIDI_INS,   type=int))
        os.environ['MOD_INGEN_NUM_MIDI_OUTS']  = str(qsettings.value(MOD_KEY_HOST_NUM_MIDI_OUTS,  MOD_DEFAULT_HOST_NUM_MIDI_OUTS,  type=int))
        os.environ['MOD_INGEN_NUM_CV_INS']     = str(qsettings.value(MOD_KEY_HOST_NUM_CV_INS,     MOD_DEFAULT_HOST_NUM_CV_INS,     type=int))
        os.environ['MOD_INGEN_NUM_CV_OUTS']    = str(qsettings.value(MOD_KEY_HOST_NUM_CV_OUTS,    MOD_DEFAULT_HOST_NUM_CV_OUTS,    type=int))

        del qsettings

    os.environ['MOD_GUI_SHOW_MODE'] = str(modguiShowMode)
    os.environ['MOD_LOG']           = "1" if webviewVerbose else "0"

    from mod import settings
    settings.MODGUI_SHOW_MODE = modguiShowMode
    settings.LOG              = webviewVerbose

    # cleanup
    del modguiShowMode, webviewVerbose

# ------------------------------------------------------------------------------------------------------------
