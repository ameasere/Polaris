# ///////////////////////////////////////////////////////////////
#
# Framework by: WANDERSON M.PIMENTA
# MADE WITH: Qt Designer and PySide6
# V: 1.0.0
#
# Developed by: Ameasere
# V: 0.0.1
#
# ///////////////////////////////////////////////////////////////

import sys
import os
import platform

# IMPORT / GUI AND MODULES AND WIDGETS
# ///////////////////////////////////////////////////////////////
from modules import *
from widgets import *

if platform.system() == "Windows":
    import ctypes
    from ctypes import c_int, c_void_p, byref

    ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID("polaris.ameasere")
else:
    import AppKit

    # Change title for Linux and Mac
    # os.environ["QT_MAC_WANTS_LAYER"] = "1"
    os.environ["QT_SCALE_FACTOR"] = "1"
    AppKit.NSBundle.mainBundle().infoDictionary().setValue_forKey_('Polaris', 'CFBundleName')

# Change DPI settings if the screen is 4K or if the scale is above 100%
# ///////////////////////////////////////////////////////////////
if platform.system() == "Windows":
    try:
        ctypes.windll.user32.SetProcessDPIAware()
        scale = ctypes.windll.shcore.GetScaleFactorForDevice(0)
        if scale > 1:
            ctypes.windll.shcore.SetProcessDpiAwareness(2)
            os.environ["QT_FONT_DPI"] = "96"  # FIX Problem for High DPI and Scale above 100%
        else:
            os.environ["QT_FONT_DPI"] = "84"
    except:
        pass
else:
    os.environ["QT_FONT_DPI"] = "84"  # FIX Problem for High DPI and Scale above 100%

# SET AS GLOBAL WIDGETS
# ///////////////////////////////////////////////////////////////
widgets = None


class MainWindow(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        # SET AS GLOBAL WIDGETS
        # ///////////////////////////////////////////////////////////////
        self.dragPos = None
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        # Get size of screen
        screen = QApplication.primaryScreen()
        size = screen.size()
        # Set size of window to 100px less than screen size in both directions
        if size.width() - 100 < 1400 or size.height() - 100 < 860:
            # noinspection PyArgumentList
            self.resize(size.width() - 400, size.height() - 400)
        global widgets
        widgets = self.ui
        titleBarEnabled = True if platform.system() == "Windows" else False
        # USE CUSTOM TITLE BAR | USE AS "False" FOR MAC OR LINUX
        # ///////////////////////////////////////////////////////////////
        Settings.ENABLE_CUSTOM_TITLE_BAR = titleBarEnabled
        if not Settings.ENABLE_CUSTOM_TITLE_BAR:
            widgets.bgApp.setStyleSheet("border-top-left-radius: 0px; border-top-right-radius: 0px;")

        # APP NAME
        # ///////////////////////////////////////////////////////////////
        title = "Polaris"
        # APPLY TEXTS
        self.setWindowTitle(title)

        # TOGGLE MENU
        # ///////////////////////////////////////////////////////////////
        widgets.toggleButton.clicked.connect(lambda: UIFunctions.toggleMenu(self, True))

        # SET UI DEFINITIONS
        # ///////////////////////////////////////////////////////////////
        UIFunctions.uiDefinitions(self)

        # QTableWidget PARAMETERS
        # ///////////////////////////////////////////////////////////////
        widgets.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        # BUTTONS CLICK
        # ///////////////////////////////////////////////////////////////

        # LEFT MENUS
        widgets.btn_home.clicked.connect(self.buttonClick)
        widgets.btn_widgets.clicked.connect(self.buttonClick)
        widgets.btn_new.clicked.connect(self.buttonClick)
        widgets.btn_save.clicked.connect(self.buttonClick)

        # widgets.settingsTopBtn.hide()

        # EXTRA LEFT BOX
        def openCloseLeftBox():
            UIFunctions.toggleLeftBox(self, True)

        widgets.toggleLeftBox.clicked.connect(openCloseLeftBox)
        widgets.extraCloseColumnBtn.clicked.connect(openCloseLeftBox)

        self.paintEvent(None)

        # SHOW APP
        # ///////////////////////////////////////////////////////////////
        self.show()

        # SET HOME PAGE AND SELECT MENU
        # ///////////////////////////////////////////////////////////////
        widgets.stackedWidget.setCurrentWidget(widgets.home)
        widgets.btn_home.setStyleSheet(UIFunctions.selectMenu(widgets.btn_home.styleSheet()))
        self.current_page = "home"
        # If the current page is "home", then change the button background image
        widgets.btn_home.setStyleSheet(
            widgets.btn_home.styleSheet() + "background-image: url(\":/icons/images/icons/home_selected.png\");")

    # BUTTONS CLICK
    # Post here your functions for clicked buttons
    # ///////////////////////////////////////////////////////////////
    def buttonClick(self):
        # GET BUTTON CLICKED
        btn = self.sender()
        btnName = btn.objectName()

        # SHOW HOME PAGE
        if btnName == "btn_home":
            widgets.stackedWidget.setCurrentWidget(widgets.home)
            UIFunctions.resetStyle(self, btnName)
            btn.setStyleSheet(UIFunctions.selectMenu(
                btn.styleSheet()) + "background-image: url(\":/icons/images/icons/home_selected.png\");")
            self.current_page = "home"

        # SHOW WIDGETS PAGE
        if btnName == "btn_widgets":
            widgets.stackedWidget.setCurrentWidget(widgets.widgets)
            UIFunctions.resetStyle(self, btnName)
            btn.setStyleSheet(UIFunctions.selectMenu(btn.styleSheet()))
            self.current_page = "widgets"
            # Replace the background image of the button
            widgets.btn_home.setStyleSheet(
                widgets.btn_home.styleSheet() + "background-image: url(\":/icons/images/icons/home_unselected.png\");")

        # SHOW NEW PAGE
        if btnName == "btn_new":
            widgets.stackedWidget.setCurrentWidget(widgets.new_page)  # SET PAGE
            UIFunctions.resetStyle(self, btnName)  # RESET ANOTHERS BUTTONS SELECTED
            btn.setStyleSheet(UIFunctions.selectMenu(btn.styleSheet()))  # SELECT MENU
            self.current_page = "new"
            # Replace the background image of the button
            widgets.btn_home.setStyleSheet(
                widgets.btn_home.styleSheet() + "background-image: url(\":/icons/images/icons/home_unselected.png\");")

        if btnName == "btn_save":
            print("Save BTN clicked!")

        # PRINT BTN NAME
        print(f'Button "{btnName}" pressed!')

    # RESIZE EVENTS
    # ///////////////////////////////////////////////////////////////
    def resizeEvent(self, event):
        # Update Size Grips
        UIFunctions.resize_grips(self)

    # MOUSE CLICK EVENTS
    # ///////////////////////////////////////////////////////////////
    def mousePressEvent(self, event):
        # SET DRAG POS WINDOW
        self.dragPos = event.globalPosition().toPoint()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon("icon.ico"))
    window = MainWindow()
    sys.exit(app.exec())
