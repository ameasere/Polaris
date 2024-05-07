# ///////////////////////////////////////////////////////////////
#
# Framework by: WANDERSON M.PIMENTA
# MADE WITH: Qt Designer and PySide6
# V: 1.0.0
#
# Developed by: Ameasere
# V: 1.0.0
#
# ///////////////////////////////////////////////////////////////

import sys
import os
import platform
import time
import json

# IMPORT / GUI AND MODULES AND WIDGETS
# ///////////////////////////////////////////////////////////////
from modules import *
from windows import LoginWindow

if platform.system() == "Windows":
    import ctypes
    from ctypes import c_int, c_void_p, byref

    ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID("polaris.ameasere")
elif platform.system() == "Darwin":
    import AppKit

    # Change title for Linux and Mac
    # os.environ["QT_MAC_WANTS_LAYER"] = "1"
    os.environ["QT_SCALE_FACTOR"] = "1"
    AppKit.NSBundle.mainBundle().infoDictionary().setValue_forKey_('Polaris', 'CFBundleName')
    AppKit.NSBundle.mainBundle().infoDictionary().setValue_forKey_('Polaris', 'CFBundleDisplayName')
    AppKit.NSBundle.mainBundle().infoDictionary().setValue_forKey_('polaris.ameasere', 'CFBundleIdentifier')
    AppKit.NSBundle.mainBundle().infoDictionary().setValue_forKey_('1.0.0', 'CFBundleShortVersionString')

# os.environ["QT_LOGGING_RULES"] = "*.debug=false;*.warning=false;*.critical=false"

# Change DPI settings if the screen is 4K or if the scale is above 100%
# ///////////////////////////////////////////////////////////////
if platform.system() == "Windows":
    try:
        ctypes.windll.user32.SetProcessDPIAware()
        scale = ctypes.windll.shcore.GetScaleFactorForDevice(0)
        if scale > 1:
            ctypes.windll.shcore.SetProcessDpiAwareness(2)
            os.environ["QT_AUTO_SCREEN_SCALE_FACTOR"] = "1"  # FIX Problem for High DPI and Scale above 100%
        else:
            os.environ["QT_FONT_DPI"] = "72"
    except:
        pass
else:
    os.environ["QT_FONT_DPI"] = "72"  # FIX Problem for High DPI and Scale above 100%

# SET AS GLOBAL WIDGETS
# ///////////////////////////////////////////////////////////////
widgets = None


def preliminary_config_check():
    if not os.path.exists(os.getcwd() + "/temp"):
        os.mkdir(os.getcwd() + "/temp")
    if os.path.exists(os.getcwd() + "/config/config.json"):
        with open(os.getcwd() + "/config/config.json", "r") as f:
            config = json.load(f)
            f.close()
        return config
    else:
        if not os.path.exists(os.getcwd() + "/config"):
            os.mkdir(os.getcwd() + "/config")
        with open(os.getcwd() + "/config/config.json", "w") as f:
            f.write("{}")
            f.close()
        return {}


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon("icon.ico"))
    config = preliminary_config_check()
    if "token" not in config or config["token"] == "":
        window = LoginWindow(window="password", config=config)
    else:
        window = LoginWindow(window="token", config=config)
    sys.exit(app.exec())
