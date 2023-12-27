# ///////////////////////////////////////////////////////////////
#
# Framework by: WANDERSON M.PIMENTA
# MADE WITH: Qt Designer and PySide6
# V: 1.0.0
#
# Developed by: Ameasere
# V: 0.3.0
#
# ///////////////////////////////////////////////////////////////

import sys
import os
import platform
import time

# IMPORT / GUI AND MODULES AND WIDGETS
# ///////////////////////////////////////////////////////////////
from modules import *

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
    AppKit.NSBundle.mainBundle().infoDictionary().setValue_forKey_('0.3.0', 'CFBundleShortVersionString')

# os.environ["QT_LOGGING_RULES"] = "*.debug=false;*.warning=false;*.critical=false"

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


class MainWindow(QMainWindow):
    def __init__(self, response):
        QMainWindow.__init__(self)
        # SET AS GLOBAL WIDGETS
        # ///////////////////////////////////////////////////////////////
        self.dragPos = None
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        # Get size of screen
        screen = QApplication.primaryScreen()
        size = screen.size()
        if isinstance(response, str):
            self.__response = json.loads(response)
        else:
            self.__response = response
        # Set size of window to 100px less than screen size in both directions
        if size.width() - 100 < 1400 or size.height() - 100 < 860:
            # noinspection PyArgumentList
            self.resize(size.width() - 400, size.height() - 400)
        # USE CUSTOM TITLE BAR | USE AS "False" FOR MAC OR LINUX
        # ///////////////////////////////////////////////////////////////
        Settings.ENABLE_CUSTOM_TITLE_BAR = True
        if not Settings.ENABLE_CUSTOM_TITLE_BAR:
            self.ui.bgApp.setStyleSheet("border-top-left-radius: 0px; border-top-right-radius: 0px;")
            self.ui.appMargins.setContentsMargins(0, 0, 0, 0)
        else:
            # STANDARD TITLE BAR
            self.setWindowFlags(Qt.FramelessWindowHint)
            self.setAttribute(Qt.WA_TranslucentBackground)

            # MOVE WINDOW / MAXIMIZE / RESTORE
            def moveWindow(event):
                # MOVE WINDOW
                if event.buttons() == Qt.LeftButton:
                    self.move(self.pos() + event.globalPosition().toPoint() - self.dragPos)
                    self.dragPos = event.globalPosition().toPoint()
                    event.accept()

            # Any dragging on the window will move it
            self.ui.dragBar.mouseMoveEvent = moveWindow
        self.shadow = QGraphicsDropShadowEffect(self)
        self.shadow.setBlurRadius(17)
        self.shadow.setXOffset(0)
        self.shadow.setYOffset(0)
        self.shadow.setColor(QColor(0, 0, 0, 150))
        self.ui.bgApp.setGraphicsEffect(self.shadow)
        # APP NAME
        # ///////////////////////////////////////////////////////////////
        title = "Polaris"
        # APPLY TEXTS
        self.setWindowTitle(title)
        self.ui.username.setText(self.__response["username"])

        self.currentPage = "dashboard"
        self.ui.pages.setCurrentWidget(self.ui.dashboard)

        self.ui.ctx_btns.hide()
        for child in self.ui.ctx_btns.children():
            child.hide()
        self.ctx_btns_state = False

        # BUTTONS CLICK
        # ///////////////////////////////////////////////////////////////

        self.ui.btn_dashboard.clicked.connect(self.buttonClick)
        self.ui.btn_documentation.clicked.connect(self.buttonClick)
        self.ui.btn_account.clicked.connect(self.buttonClick)
        self.ui.btn_settings.clicked.connect(self.buttonClick)
        self.ui.btn_dropdown.clicked.connect(self.buttonClick)
        self.ui.btn_close.clicked.connect(self.buttonClick)
        self.ui.btn_minimize.clicked.connect(self.buttonClick)
        self.ui.btn_logout.clicked.connect(self.buttonClick)

        # widgets.settingsTopBtn.hide()

        self.paintEvent(None)

        if "stafficon" in self.__response:
            icon = self.__response["stafficon"].encode("utf-8")
            # Write the image to a file in the temp folder, and set in stylesheet dynamically
            with open(os.getcwd() + "/temp/icon.png", "wb") as f:
                f.write(base64.b64decode(icon))
                f.close()
            path = os.getcwd() + "/temp/icon.png"
            path = path.replace("\\", "/")
            # Set as pixmap
            self.ui.profilepic.setPixmap(QPixmap(path))
        # If the subscription JSON object is not empty
        elif "icon" in self.__response["subscription"]:
            icon = self.__response["subscription"]["icon"].encode("utf-8")
            with open(os.getcwd() + "/temp/icon.png", "wb") as f:
                f.write(base64.b64decode(icon))
                f.close()
            path = os.getcwd() + "/temp/icon.png"
            path = path.replace("\\", "/")
            self.ui.profilepic.setPixmap(QPixmap(path))
        else:
            self.ui.profilepic.setPixmap(QPixmap(":/icons/images/icons/user.png"))

        try:
            # IP is the "response" element of JSON from server
            ipaddr = json.loads(requests.get("https://api.ameasere.com/polaris/ip").text)["response"]
        except:
            # Get the local IP address instead
            ipaddr = socket.gethostbyname(socket.gethostname())

        self.ui.ipaddress.setText(ipaddr)

        # SHOW APP
        # ///////////////////////////////////////////////////////////////
        self.show()
        self.setWindowOpacity(0.0)
        self.fadeInAnimation = QPropertyAnimation(self, b"windowOpacity")
        self.fadeInAnimation.setDuration(350)
        self.fadeInAnimation.setStartValue(0)
        self.fadeInAnimation.setEndValue(1)
        self.fadeInAnimation.setEasingCurve(QEasingCurve.InOutQuart)
        self.fadeInAnimation.start()

        # SET HOME PAGE AND SELECT MENU
        # ///////////////////////////////////////////////////////////////
        # self.ui.stackedWidget.setCurrentWidget(self.ui.home)

        self.dashboard_selected_stylesheet = "I2J0bl9kYXNoYm9hcmQgewpiYWNrZ3JvdW5kLWNvbG9yOiB0cmFuc3BhcmVudDsKZm9udDogNjAwIDEwcHQgIkludGVyIE1lZGl1bSI7CnRleHQtYWxpZ246IGxlZnQ7CmNvbG9yOiAjZmZmOwpib3JkZXItcmFkaXVzOiA1cHg7Cn0KI2J0bl9kYXNoYm9hcmQ6aG92ZXIgewpiYWNrZ3JvdW5kLWNvbG9yOiB0cmFuc3BhcmVudDsKZm9udDogNjAwIDEwcHQgIkludGVyIE1lZGl1bSI7CnRleHQtYWxpZ246IGxlZnQ7CmNvbG9yOiAjZmZmOwpib3JkZXItcmFkaXVzOiA1cHg7Cn0KI2J0bl9kYXNoYm9hcmQ6cHJlc3NlZCB7CmJhY2tncm91bmQtY29sb3I6IHRyYW5zcGFyZW50Owpmb250OiA2MDAgMTBwdCAiSW50ZXIgTWVkaXVtIjsKdGV4dC1hbGlnbjogbGVmdDsKY29sb3I6ICM5ZTc3ZWQ7CmJvcmRlci1yYWRpdXM6IDVweDsKfQ=="
        self.dashboard_unselected_stylesheet = "I2J0bl9kYXNoYm9hcmQgewpiYWNrZ3JvdW5kLWNvbG9yOiB0cmFuc3BhcmVudDsKZm9udDogNjAwIDEwcHQgIkludGVyIE1lZGl1bSI7CnRleHQtYWxpZ246IGxlZnQ7CmNvbG9yOiAjQTI5RjlGOwpib3JkZXItcmFkaXVzOiA1cHg7Cn0KI2J0bl9kYXNoYm9hcmQ6aG92ZXIgewpiYWNrZ3JvdW5kLWNvbG9yOiB0cmFuc3BhcmVudDsKZm9udDogNjAwIDEwcHQgIkludGVyIE1lZGl1bSI7CnRleHQtYWxpZ246IGxlZnQ7CmNvbG9yOiAjZmZmOwpib3JkZXItcmFkaXVzOiA1cHg7Cn0KI2J0bl9kYXNoYm9hcmQ6cHJlc3NlZCB7CmJhY2tncm91bmQtY29sb3I6IHRyYW5zcGFyZW50Owpmb250OiA2MDAgMTBwdCAiSW50ZXIgTWVkaXVtIjsKdGV4dC1hbGlnbjogbGVmdDsKY29sb3I6ICM5ZTc3ZWQ7CmJvcmRlci1yYWRpdXM6IDVweDsKfQ=="

        self.documentation_selected_stylesheet = "I2J0bl9kb2N1bWVudGF0aW9uIHsKYmFja2dyb3VuZC1jb2xvcjogdHJhbnNwYXJlbnQ7CmZvbnQ6IDYwMCAxMHB0ICJJbnRlciBNZWRpdW0iOwp0ZXh0LWFsaWduOiBsZWZ0Owpjb2xvcjogI2ZmZjsKYm9yZGVyLXJhZGl1czogNXB4Owp9CiNidG5fZG9jdW1lbnRhdGlvbjpob3ZlciB7CmJhY2tncm91bmQtY29sb3I6IHRyYW5zcGFyZW50Owpmb250OiA2MDAgMTBwdCAiSW50ZXIgTWVkaXVtIjsKdGV4dC1hbGlnbjogbGVmdDsKY29sb3I6ICNmZmY7CmJvcmRlci1yYWRpdXM6IDVweDsKfQojYnRuX2RvY3VtZW50YXRpb246cHJlc3NlZCB7CmJhY2tncm91bmQtY29sb3I6IHRyYW5zcGFyZW50Owpmb250OiA2MDAgMTBwdCAiSW50ZXIgTWVkaXVtIjsKdGV4dC1hbGlnbjogbGVmdDsKY29sb3I6ICM5ZTc3ZWQ7CmJvcmRlci1yYWRpdXM6IDVweDsKfQ=="
        self.documentation_unselected_stylesheet = "I2J0bl9kb2N1bWVudGF0aW9uIHsKYmFja2dyb3VuZC1jb2xvcjogdHJhbnNwYXJlbnQ7CmZvbnQ6IDYwMCAxMHB0ICJJbnRlciBNZWRpdW0iOwp0ZXh0LWFsaWduOiBsZWZ0Owpjb2xvcjogI0EyOUY5RjsKYm9yZGVyLXJhZGl1czogNXB4Owp9CiNidG5fZG9jdW1lbnRhdGlvbjpob3ZlciB7CmJhY2tncm91bmQtY29sb3I6IHRyYW5zcGFyZW50Owpmb250OiA2MDAgMTBwdCAiSW50ZXIgTWVkaXVtIjsKdGV4dC1hbGlnbjogbGVmdDsKY29sb3I6ICNmZmY7CmJvcmRlci1yYWRpdXM6IDVweDsKfQojYnRuX2RvY3VtZW50YXRpb246cHJlc3NlZCB7CmJhY2tncm91bmQtY29sb3I6IHRyYW5zcGFyZW50Owpmb250OiA2MDAgMTBwdCAiSW50ZXIgTWVkaXVtIjsKdGV4dC1hbGlnbjogbGVmdDsKY29sb3I6ICM5ZTc3ZWQ7CmJvcmRlci1yYWRpdXM6IDVweDsKfQ=="

        self.account_selected_stylesheet = "I2J0bl9hY2NvdW50IHsKYmFja2dyb3VuZC1jb2xvcjogdHJhbnNwYXJlbnQ7CmZvbnQ6IDYwMCAxMHB0ICJJbnRlciBNZWRpdW0iOwp0ZXh0LWFsaWduOiBsZWZ0Owpjb2xvcjogI2ZmZjsKYm9yZGVyLXJhZGl1czogNXB4Owp9CiNidG5fYWNjb3VudDpob3ZlciB7CmJhY2tncm91bmQtY29sb3I6IHRyYW5zcGFyZW50Owpmb250OiA2MDAgMTBwdCAiSW50ZXIgTWVkaXVtIjsKdGV4dC1hbGlnbjogbGVmdDsKY29sb3I6ICNmZmY7CmJvcmRlci1yYWRpdXM6IDVweDsKfQojYnRuX2FjY291bnQ6cHJlc3NlZCB7CmJhY2tncm91bmQtY29sb3I6IHRyYW5zcGFyZW50Owpmb250OiA2MDAgMTBwdCAiSW50ZXIgTWVkaXVtIjsKdGV4dC1hbGlnbjogbGVmdDsKY29sb3I6ICM5ZTc3ZWQ7CmJvcmRlci1yYWRpdXM6IDVweDsKfQ=="
        self.account_unselected_stylesheet = "I2J0bl9hY2NvdW50IHsKYmFja2dyb3VuZC1jb2xvcjogdHJhbnNwYXJlbnQ7CmZvbnQ6IDYwMCAxMHB0ICJJbnRlciBNZWRpdW0iOwp0ZXh0LWFsaWduOiBsZWZ0Owpjb2xvcjogI0EyOUY5RjsKYm9yZGVyLXJhZGl1czogNXB4Owp9CiNidG5fYWNjb3VudDpob3ZlciB7CmJhY2tncm91bmQtY29sb3I6IHRyYW5zcGFyZW50Owpmb250OiA2MDAgMTBwdCAiSW50ZXIgTWVkaXVtIjsKdGV4dC1hbGlnbjogbGVmdDsKY29sb3I6ICNmZmY7CmJvcmRlci1yYWRpdXM6IDVweDsKfQojYnRuX2FjY291bnQ6cHJlc3NlZCB7CmJhY2tncm91bmQtY29sb3I6IHRyYW5zcGFyZW50Owpmb250OiA2MDAgMTBwdCAiSW50ZXIgTWVkaXVtIjsKdGV4dC1hbGlnbjogbGVmdDsKY29sb3I6ICM5ZTc3ZWQ7CmJvcmRlci1yYWRpdXM6IDVweDsKfQ=="

        self.settings_selected_stylesheet = "I2J0bl9zZXR0aW5ncyB7CmJhY2tncm91bmQtY29sb3I6IHRyYW5zcGFyZW50Owpmb250OiA2MDAgMTBwdCAiSW50ZXIgTWVkaXVtIjsKdGV4dC1hbGlnbjogbGVmdDsKY29sb3I6ICNmZmY7CmJvcmRlci1yYWRpdXM6IDVweDsKfQojYnRuX3NldHRpbmdzOmhvdmVyIHsKYmFja2dyb3VuZC1jb2xvcjogdHJhbnNwYXJlbnQ7CmZvbnQ6IDYwMCAxMHB0ICJJbnRlciBNZWRpdW0iOwp0ZXh0LWFsaWduOiBsZWZ0Owpjb2xvcjogI2ZmZjsKYm9yZGVyLXJhZGl1czogNXB4Owp9CiNidG5fc2V0dGluZ3M6cHJlc3NlZCB7CmJhY2tncm91bmQtY29sb3I6IHRyYW5zcGFyZW50Owpmb250OiA2MDAgMTBwdCAiSW50ZXIgTWVkaXVtIjsKdGV4dC1hbGlnbjogbGVmdDsKY29sb3I6ICM5ZTc3ZWQ7CmJvcmRlci1yYWRpdXM6IDVweDsKfQ=="
        self.settings_unselected_stylesheet = "I2J0bl9zZXR0aW5ncyB7CmJhY2tncm91bmQtY29sb3I6IHRyYW5zcGFyZW50Owpmb250OiA2MDAgMTBwdCAiSW50ZXIgTWVkaXVtIjsKdGV4dC1hbGlnbjogbGVmdDsKY29sb3I6ICNBMjlGOUY7CmJvcmRlci1yYWRpdXM6IDVweDsKfQojYnRuX3NldHRpbmdzOmhvdmVyIHsKYmFja2dyb3VuZC1jb2xvcjogdHJhbnNwYXJlbnQ7CmZvbnQ6IDYwMCAxMHB0ICJJbnRlciBNZWRpdW0iOwp0ZXh0LWFsaWduOiBsZWZ0Owpjb2xvcjogI2ZmZjsKYm9yZGVyLXJhZGl1czogNXB4Owp9CiNidG5fc2V0dGluZ3M6cHJlc3NlZCB7CmJhY2tncm91bmQtY29sb3I6IHRyYW5zcGFyZW50Owpmb250OiA2MDAgMTBwdCAiSW50ZXIgTWVkaXVtIjsKdGV4dC1hbGlnbjogbGVmdDsKY29sb3I6ICM5ZTc3ZWQ7CmJvcmRlci1yYWRpdXM6IDVweDsKfQ=="

    # BUTTONS CLICK
    # Post here your functions for clicked buttons
    # ///////////////////////////////////////////////////////////////
    def buttonClick(self):
        # GET BUTTON CLICKED
        btn = self.sender()
        btnName = btn.objectName()

        if btnName == "btn_minimize":
            self.showMinimized()

        elif btnName == "btn_close":
            self.close()

        elif btnName == "btn_dropdown":
            if self.ctx_btns_state:
                self.ctx_btns_state = False
                self.fadeOutChildren()
                self.ui.btn_dropdown.setIcon(QIcon(":/icons/images/icons/arrow-down-left.png"))
            else:
                self.ui.ctx_btns.show()
                self.ctx_btns_state = True
                self.fadeInChildren()
                self.ui.btn_dropdown.setIcon(QIcon(":/icons/images/icons/arrow-up-right.png"))

        # SHOW NEW PAGE
        if btnName == "btn_documentation":
            if self.currentPage != "documentation":
                # Reset stylesheet of the current page's button
                match self.currentPage:
                    case ("dashboard"):
                        self.ui.btn_dashboard.setStyleSheet(
                            base64.b64decode(self.dashboard_unselected_stylesheet).decode("utf-8"))
                        self.ui.sep1.setPixmap(QPixmap(":/icons/images/icons/separator_inactive.png"))
                        self.ui.icon_1.setPixmap(QPixmap(":/icons/images/icons/home_unselected.png"))
                    case ("account"):
                        self.ui.btn_account.setStyleSheet(
                            base64.b64decode(self.account_unselected_stylesheet).decode("utf-8"))
                        self.ui.sep3.setPixmap(QPixmap(":/icons/images/icons/separator_inactive.png"))
                        self.ui.icon_3.setPixmap(QPixmap(":/icons/images/icons/user.png"))
                    case ("settings"):
                        self.ui.btn_settings.setStyleSheet(
                            base64.b64decode(self.settings_unselected_stylesheet).decode("utf-8"))
                        self.ui.sep4.setPixmap(QPixmap(":/icons/images/icons/separator_inactive.png"))
                        self.ui.icon_4.setPixmap(QPixmap(":/icons/images/icons/settings.png"))
                self.ui.pages.setCurrentWidget(self.ui.documentation)  # SET PAGE
                self.currentPage = "documentation"
                self.ui.btn_documentation.setStyleSheet(
                    base64.b64decode(self.documentation_selected_stylesheet).decode("utf-8"))
                self.ui.sep2.setPixmap(QPixmap(":/icons/images/icons/separator.png"))
                self.ui.icon_2.setPixmap(QPixmap(":/icons/images/icons/edit_selected.png"))
        elif btnName == "btn_dashboard":
            if self.currentPage != "dashboard":
                # Reset stylesheet of the current page's button
                match self.currentPage:
                    case ("documentation"):
                        self.ui.btn_documentation.setStyleSheet(
                            base64.b64decode(self.documentation_unselected_stylesheet).decode("utf-8"))
                        self.ui.sep2.setPixmap(QPixmap(":/icons/images/icons/separator_inactive.png"))
                        self.ui.icon_2.setPixmap(QPixmap(":/icons/images/icons/edit_unselected.png"))
                    case ("account"):
                        self.ui.btn_account.setStyleSheet(
                            base64.b64decode(self.account_unselected_stylesheet).decode("utf-8"))
                        self.ui.sep3.setPixmap(QPixmap(":/icons/images/icons/separator_inactive.png"))
                        self.ui.icon_3.setPixmap(QPixmap(":/icons/images/icons/user.png"))
                    case ("settings"):
                        self.ui.btn_settings.setStyleSheet(
                            base64.b64decode(self.settings_unselected_stylesheet).decode("utf-8"))
                        self.ui.sep4.setPixmap(QPixmap(":/icons/images/icons/separator_inactive.png"))
                        self.ui.icon_4.setPixmap(QPixmap(":/icons/images/icons/settings.png"))
                self.ui.pages.setCurrentWidget(self.ui.dashboard)
                self.currentPage = "dashboard"
                self.ui.btn_dashboard.setStyleSheet(
                    base64.b64decode(self.dashboard_selected_stylesheet).decode("utf-8"))
                self.ui.sep1.setPixmap(QPixmap(":/icons/images/icons/separator.png"))
                self.ui.icon_1.setPixmap(QPixmap(":/icons/images/icons/home_selected.png"))
        elif btnName == "btn_account":
            if self.currentPage != "account":
                # Reset stylesheet of the current page's button
                match self.currentPage:
                    case ("documentation"):
                        self.ui.btn_documentation.setStyleSheet(
                            base64.b64decode(self.documentation_unselected_stylesheet).decode("utf-8"))
                        self.ui.sep2.setPixmap(QPixmap(":/icons/images/icons/separator_inactive.png"))
                        self.ui.icon_2.setPixmap(QPixmap(":/icons/images/icons/edit_unselected.png"))
                    case ("dashboard"):
                        self.ui.btn_dashboard.setStyleSheet(
                            base64.b64decode(self.dashboard_unselected_stylesheet).decode("utf-8"))
                        self.ui.sep1.setPixmap(QPixmap(":/icons/images/icons/separator_inactive.png"))
                        self.ui.icon_1.setPixmap(QPixmap(":/icons/images/icons/home_unselected.png"))
                    case ("settings"):
                        self.ui.btn_settings.setStyleSheet(
                            base64.b64decode(self.settings_unselected_stylesheet).decode("utf-8"))
                        self.ui.sep4.setPixmap(QPixmap(":/icons/images/icons/separator_inactive.png"))
                        self.ui.icon_4.setPixmap(QPixmap(":/icons/images/icons/settings.png"))
                self.ui.pages.setCurrentWidget(self.ui.account)
                self.currentPage = "account"
                self.ui.btn_account.setStyleSheet(base64.b64decode(self.account_selected_stylesheet).decode("utf-8"))
                self.ui.sep3.setPixmap(QPixmap(":/icons/images/icons/separator.png"))
                self.ui.icon_3.setPixmap(QPixmap(":/icons/images/icons/user_selected.png"))
        elif btnName == "btn_settings":
            if self.currentPage != "settings":
                # Reset stylesheet of the current page's button
                match self.currentPage:
                    case ("documentation"):
                        self.ui.btn_documentation.setStyleSheet(
                            base64.b64decode(self.documentation_unselected_stylesheet).decode("utf-8"))
                        self.ui.sep2.setPixmap(QPixmap(":/icons/images/icons/separator_inactive.png"))
                        self.ui.icon_2.setPixmap(QPixmap(":/icons/images/icons/edit_unselected.png"))
                    case ("dashboard"):
                        self.ui.btn_dashboard.setStyleSheet(
                            base64.b64decode(self.dashboard_unselected_stylesheet).decode("utf-8"))
                        self.ui.sep1.setPixmap(QPixmap(":/icons/images/icons/separator_inactive.png"))
                        self.ui.icon_1.setPixmap(QPixmap(":/icons/images/icons/home_unselected.png"))
                    case ("account"):
                        self.ui.btn_account.setStyleSheet(
                            base64.b64decode(self.account_unselected_stylesheet).decode("utf-8"))
                        self.ui.sep3.setPixmap(QPixmap(":/icons/images/icons/separator_inactive.png"))
                        self.ui.icon_3.setPixmap(QPixmap(":/icons/images/icons/user.png"))
                self.ui.pages.setCurrentWidget(self.ui.settings)
                self.currentPage = "settings"
                self.ui.btn_settings.setStyleSheet(base64.b64decode(self.settings_selected_stylesheet).decode("utf-8"))
                self.ui.sep4.setPixmap(QPixmap(":/icons/images/icons/separator.png"))
                self.ui.icon_4.setPixmap(QPixmap(":/icons/images/icons/settings_selected.png"))
        elif btnName == "btn_logout":
            self.__response = None
            self.fadeout()

    def fadeout(self):
        config = preliminary_config_check()
        if "token" not in config or config["token"] == "":
            window = FirstRunWindow()
        else:
            window = TokenLoginWindow()

        def loginWindowOpener():
            # Fade out animation
            self.fadeOutAnimation = QPropertyAnimation(self, b"windowOpacity")
            self.fadeOutAnimation.setDuration(350)
            self.fadeOutAnimation.setStartValue(1)
            self.fadeOutAnimation.setEndValue(0)
            self.fadeOutAnimation.setEasingCurve(QEasingCurve.InOutQuart)
            # Start after a QTimer of 1 second
            self.timer = QTimer(self)
            self.timer.singleShot(200, lambda: self.fadeOutAnimation.start())
            self.fadeOutAnimation.finished.connect(lambda: window.fadein)

        loginWindowOpener()

    # MOUSE CLICK EVENTS
    # ///////////////////////////////////////////////////////////////
    def mousePressEvent(self, event):
        # SET DRAG POS WINDOW
        self.dragPos = event.globalPosition().toPoint()

    def fadeInChildren(self):
        def children_animations():
            self.usernameLabelAnimation.start()
            self.ui.username.show()
            self.profilepicAnimation.start()
            self.ui.profilepic.show()
            self.currentlyloggedinAnimation.start()
            self.ui.currentlyloggedin.show()
            self.ipaddressAnimation.start()
            self.ui.ipaddress.show()
            self.ui.btn_close.show()
            self.ui.btn_minimize.show()
            self.ui.divider.show()
            self.ui.btn_logout.show()

        # If any of the animations are running, stop them
        try:
            if self.usernameLabelAnimation.state() == QAbstractAnimation.Running:
                self.usernameLabelAnimation.stop()
                self.usernameLabelAnimation.setCurrentTime(0)  # Reset the animation to the beginning

            if self.profilepicAnimation.state() == QAbstractAnimation.Running:
                self.profilepicAnimation.stop()
                self.profilepicAnimation.setCurrentTime(0)

            if self.currentlyloggedinAnimation.state() == QAbstractAnimation.Running:
                self.currentlyloggedinAnimation.stop()
                self.currentlyloggedinAnimation.setCurrentTime(0)

            if self.ipaddressAnimation.state() == QAbstractAnimation.Running:
                self.ipaddressAnimation.stop()
                self.ipaddressAnimation.setCurrentTime(0)

            if self.dropdown_geometry_animation.state() == QAbstractAnimation.Running:
                self.dropdown_geometry_animation.stop()
                self.dropdown_geometry_animation.setCurrentTime(0)

            if self.fadeInAnimation.state() == QAbstractAnimation.Running:
                self.fadeInAnimation.stop()
                self.fadeInAnimation.setCurrentTime(0)

        except AttributeError:
            pass

        self.username_label_opacity_effect = QGraphicsOpacityEffect(self.ui.username)
        self.ui.username.setGraphicsEffect(self.username_label_opacity_effect)
        self.username_label_opacity_effect.setOpacity(0)

        self.usernameLabelAnimation = QPropertyAnimation(self.username_label_opacity_effect, b"opacity")
        self.usernameLabelAnimation.setDuration(500)
        self.usernameLabelAnimation.setStartValue(0)
        self.usernameLabelAnimation.setEndValue(1)
        self.usernameLabelAnimation.setEasingCurve(QEasingCurve.InOutQuart)
        self.usernameLabelAnimation.finished.connect(lambda: self.ui.username.setFocus())
        self.usernameLabelAnimation.finished.connect(lambda: self.ui.username.setGraphicsEffect(None))

        self.ui.profilepic_opacity_effect = QGraphicsOpacityEffect(self.ui.profilepic)
        self.ui.profilepic.setGraphicsEffect(self.ui.profilepic_opacity_effect)
        self.ui.profilepic_opacity_effect.setOpacity(0)

        self.profilepicAnimation = QPropertyAnimation(self.ui.profilepic_opacity_effect, b"opacity")
        self.profilepicAnimation.setDuration(500)
        self.profilepicAnimation.setStartValue(0)
        self.profilepicAnimation.setEndValue(1)
        self.profilepicAnimation.setEasingCurve(QEasingCurve.InOutQuart)

        self.currentlyloggedin_opacity_effect = QGraphicsOpacityEffect(self.ui.currentlyloggedin)
        self.ui.currentlyloggedin.setGraphicsEffect(self.currentlyloggedin_opacity_effect)
        self.currentlyloggedin_opacity_effect.setOpacity(0)

        self.currentlyloggedinAnimation = QPropertyAnimation(self.currentlyloggedin_opacity_effect, b"opacity")
        self.currentlyloggedinAnimation.setDuration(500)
        self.currentlyloggedinAnimation.setStartValue(0)
        self.currentlyloggedinAnimation.setEndValue(1)
        self.currentlyloggedinAnimation.setEasingCurve(QEasingCurve.InOutQuart)
        self.currentlyloggedinAnimation.finished.connect(lambda: self.ui.currentlyloggedin.setGraphicsEffect(None))

        self.ipaddress_opacity_effect = QGraphicsOpacityEffect(self.ui.ipaddress)
        self.ui.ipaddress.setGraphicsEffect(self.ipaddress_opacity_effect)
        self.ipaddress_opacity_effect.setOpacity(0)

        self.ipaddressAnimation = QPropertyAnimation(self.ipaddress_opacity_effect, b"opacity")
        self.ipaddressAnimation.setDuration(500)
        self.ipaddressAnimation.setStartValue(0)
        self.ipaddressAnimation.setEndValue(1)
        self.ipaddressAnimation.setEasingCurve(QEasingCurve.InOutQuart)
        self.ipaddressAnimation.finished.connect(lambda: self.ui.ipaddress.setGraphicsEffect(None))

        self.ui.ctx_btns.show()
        self.dropdown_geometry_animation = QPropertyAnimation(self.ui.ctx_btns, b"geometry")
        self.dropdown_geometry_animation.setDuration(500)
        # Start at (1232, 0, 0, 0), and extend to (1071, 20, 161, 161)
        self.dropdown_geometry_animation.setStartValue(QRect(1216, 25, 0, 0))
        self.dropdown_geometry_animation.setEndValue(QRect(1071, 20, 161, 161))
        self.dropdown_geometry_animation.setEasingCurve(QEasingCurve.InOutQuart)
        self.dropdown_geometry_animation.start()
        self.dropdown_geometry_animation.finished.connect(lambda: children_animations())

    def fadeOutChildren(self):
        def children_animations():
            for child in self.ui.ctx_btns.children():
                child.hide()

        children_animations()
        try:
            if self.dropdown_geometry_animation_reverse.state() == QAbstractAnimation.Running:
                self.dropdown_geometry_animation_reverse.stop()
                self.dropdown_geometry_animation_reverse.setCurrentTime(0)
        except AttributeError:
            pass

        self.dropdown_geometry_animation_reverse = QPropertyAnimation(self.ui.ctx_btns, b"geometry")
        self.dropdown_geometry_animation_reverse.setDuration(500)
        # Start at (1071, 20, 161, 161), and extend to (1232, 0, 0, 0)
        self.dropdown_geometry_animation_reverse.setStartValue(QRect(1071, 20, 161, 161))
        self.dropdown_geometry_animation_reverse.setEndValue(QRect(1216, 25, 0, 0))
        self.dropdown_geometry_animation_reverse.setEasingCurve(QEasingCurve.InOutQuart)
        self.dropdown_geometry_animation_reverse.start()


class FirstRunWindow(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        # SET AS GLOBAL WIDGETS
        # ///////////////////////////////////////////////////////////////
        self.dragPos = None
        self.ui = Ui_PasswordLoginWindow()
        self.ui.setupUi(self)
        widgets = self.ui

        # USE CUSTOM TITLE BAR | USE AS "False" FOR MAC OR LINUX
        # ///////////////////////////////////////////////////////////////
        Settings.ENABLE_CUSTOM_TITLE_BAR = True
        if not Settings.ENABLE_CUSTOM_TITLE_BAR:
            widgets.bgApp.setStyleSheet("border-top-left-radius: 0px; border-top-right-radius: 0px;")
            self.ui.appMargins.setContentsMargins(0, 0, 0, 0)
            self.ui.btn_minimize.hide()
            self.ui.btn_close.hide()
        else:
            # STANDARD TITLE BAR
            self.setWindowFlags(Qt.FramelessWindowHint)
            self.setAttribute(Qt.WA_TranslucentBackground)

            # MOVE WINDOW / MAXIMIZE / RESTORE
            def moveWindow(event):
                # IF MAXIMIZED CHANGE TO NORMAL
                # MOVE WINDOW
                if event.buttons() == Qt.LeftButton:
                    self.move(self.pos() + event.globalPosition().toPoint() - self.dragPos)
                    self.dragPos = event.globalPosition().toPoint()
                    event.accept()

            self.ui.dragBar.mouseMoveEvent = moveWindow
        self.shadow = QGraphicsDropShadowEffect(self)
        self.shadow.setBlurRadius(17)
        self.shadow.setXOffset(0)
        self.shadow.setYOffset(0)
        self.shadow.setColor(QColor(0, 0, 0, 150))
        self.ui.bgApp.setGraphicsEffect(self.shadow)
        self.ui.btn_minimize.clicked.connect(lambda: self.showMinimized())

        # CLOSE APPLICATION
        self.ui.btn_close.clicked.connect(lambda: self.close())

        # APP NAME
        # ///////////////////////////////////////////////////////////////
        title = "Polaris"
        # APPLY TEXTS
        self.setWindowTitle(title)

        self.ui.usernameLabel.hide()
        self.ui.username.hide()
        self.ui.passwordLabel.hide()
        self.ui.password.hide()

        # LEFT MENUS
        widgets.login_button.clicked.connect(self.buttonClick)
        widgets.register_button.clicked.connect(self.buttonClick)

        # widgets.settingsTopBtn.hide()

        self.paintEvent(None)

        # SHOW APP
        # ///////////////////////////////////////////////////////////////
        self.show()

        # SET HOME PAGE AND SELECT MENU
        # ///////////////////////////////////////////////////////////////
        widgets.pages.setCurrentWidget(widgets.login)

        self.backgroundAnimation = QPropertyAnimation(self.ui.bg1, b"geometry")
        self.backgroundAnimation.setDuration(800)
        self.backgroundAnimation.setStartValue(QRect(0, 0, 31, 501))
        self.backgroundAnimation.setEndValue(QRect(0, 0, 310, 501))
        self.backgroundAnimation.setEasingCurve(QEasingCurve.InOutQuart)
        self.backgroundAnimation.start()

        self.username_label_opacity_effect = QGraphicsOpacityEffect(self.ui.usernameLabel)
        self.ui.usernameLabel.setGraphicsEffect(self.username_label_opacity_effect)
        self.username_label_opacity_effect.setOpacity(0)

        self.usernameLabelAnimation = QPropertyAnimation(self.username_label_opacity_effect, b"opacity")
        self.usernameLabelAnimation.setDuration(500)
        self.usernameLabelAnimation.setStartValue(0)
        self.usernameLabelAnimation.setEndValue(1)
        self.usernameLabelAnimation.setEasingCurve(QEasingCurve.InOutQuart)
        self.usernameLabelAnimation.finished.connect(lambda: self.ui.username.setFocus())
        self.usernameLabelAnimation.finished.connect(lambda: self.ui.usernameLabel.setGraphicsEffect(None))
        self.usernameLabelAnimation.start()
        self.ui.usernameLabel.show()

        self.username_opacity_effect = QGraphicsOpacityEffect(self.ui.username)
        self.ui.username.setGraphicsEffect(self.username_opacity_effect)
        self.username_opacity_effect.setOpacity(0)

        self.username_shadow = QGraphicsDropShadowEffect(self.ui.username)
        self.username_shadow.setBlurRadius(17)
        self.username_shadow.setXOffset(0)
        self.username_shadow.setYOffset(0)
        self.username_shadow.setColor(QColor(0, 0, 0, 150))

        self.usernameAnimation = QPropertyAnimation(self.username_opacity_effect, b"opacity")
        self.usernameAnimation.setDuration(500)
        self.usernameAnimation.setStartValue(0)
        self.usernameAnimation.setEndValue(1)
        self.usernameAnimation.setEasingCurve(QEasingCurve.InOutQuart)
        self.usernameAnimation.finished.connect(lambda: self.ui.username.setGraphicsEffect(self.username_shadow))
        self.usernameAnimation.start()
        self.ui.username.show()

        self.password_label_opacity_effect = QGraphicsOpacityEffect(self.ui.passwordLabel)
        self.ui.passwordLabel.setGraphicsEffect(self.password_label_opacity_effect)
        self.password_label_opacity_effect.setOpacity(0)

        self.passwordLabelAnimation = QPropertyAnimation(self.password_label_opacity_effect, b"opacity")
        self.passwordLabelAnimation.setDuration(500)
        self.passwordLabelAnimation.setStartValue(0)
        self.passwordLabelAnimation.setEndValue(1)
        self.passwordLabelAnimation.setEasingCurve(QEasingCurve.InOutQuart)
        self.passwordLabelAnimation.finished.connect(lambda: self.ui.passwordLabel.setGraphicsEffect(None))
        self.passwordLabelAnimation.start()
        self.ui.passwordLabel.show()

        self.password_opacity_effect = QGraphicsOpacityEffect(self.ui.password)
        self.ui.password.setGraphicsEffect(self.password_opacity_effect)
        self.password_opacity_effect.setOpacity(0)

        self.password_shadow = QGraphicsDropShadowEffect(self.ui.password)
        self.password_shadow.setBlurRadius(17)
        self.password_shadow.setXOffset(0)
        self.password_shadow.setYOffset(0)
        self.password_shadow.setColor(QColor(0, 0, 0, 150))

        self.passwordAnimation = QPropertyAnimation(self.password_opacity_effect, b"opacity")
        self.passwordAnimation.setDuration(500)
        self.passwordAnimation.setStartValue(0)
        self.passwordAnimation.setEndValue(1)
        self.passwordAnimation.setEasingCurve(QEasingCurve.InOutQuart)
        self.passwordAnimation.finished.connect(lambda: self.ui.password.setGraphicsEffect(self.password_shadow))
        self.passwordAnimation.start()
        self.ui.password.show()

        self.response_label_animation = QPropertyAnimation(self.ui.responseLabel, b"geometry")
        self.response_label_animation.setDuration(500)
        self.response_label_animation.setStartValue(QRect(0, 511, 351, 0))
        self.response_label_animation.setEndValue(QRect(0, 460, 351, 41))
        self.response_label_animation.setEasingCurve(QEasingCurve.InBounce)

        self.response_label_animation_reverse = QPropertyAnimation(self.ui.responseLabel, b"geometry")
        self.response_label_animation_reverse.setDuration(500)
        self.response_label_animation_reverse.setStartValue(QRect(0, 460, 351, 41))
        self.response_label_animation_reverse.setEndValue(QRect(0, 511, 351, 0))
        self.response_label_animation_reverse.setEasingCurve(QEasingCurve.OutBounce)
        self.response_label_animation_reverse.finished.connect(lambda: self.updateEverything)

        self.twofactor_responselabel_animation = QPropertyAnimation(self.ui.twofactor_responselabel, b"geometry")
        self.twofactor_responselabel_animation.setDuration(500)
        self.twofactor_responselabel_animation.setStartValue(QRect(0, 511, 351, 0))
        self.twofactor_responselabel_animation.setEndValue(QRect(0, 460, 351, 41))
        self.twofactor_responselabel_animation.setEasingCurve(QEasingCurve.InBounce)

        self.twofactor_responselabel_reverse = QPropertyAnimation(self.ui.twofactor_responselabel, b"geometry")
        self.twofactor_responselabel_reverse.setDuration(500)
        self.twofactor_responselabel_reverse.setStartValue(QRect(0, 460, 351, 41))
        self.twofactor_responselabel_reverse.setEndValue(QRect(0, 511, 351, 0))
        self.twofactor_responselabel_reverse.setEasingCurve(QEasingCurve.OutBounce)
        self.twofactor_responselabel_reverse.finished.connect(lambda: self.updateEverything)

        self.twofactor_field_opacity_effect = QGraphicsOpacityEffect(self.ui.twofactor_field)
        self.ui.twofactor_field.setGraphicsEffect(self.twofactor_field_opacity_effect)
        self.twofactor_field_opacity_effect.setOpacity(0)

        self.twofactor_button_opacity_effect = QGraphicsOpacityEffect(self.ui.twofactor_button)
        self.ui.twofactor_button.setGraphicsEffect(self.twofactor_button_opacity_effect)
        self.twofactor_button_opacity_effect.setOpacity(0)

        self.tff_shadow = QGraphicsDropShadowEffect(self.ui.twofactor_field)
        self.tff_shadow.setBlurRadius(17)
        self.tff_shadow.setXOffset(0)
        self.tff_shadow.setYOffset(0)
        self.tff_shadow.setColor(QColor(0, 0, 0, 150))

        self.tfb_shadow = QGraphicsDropShadowEffect(self.ui.twofactor_button)
        self.tfb_shadow.setBlurRadius(17)
        self.tfb_shadow.setXOffset(0)
        self.tfb_shadow.setYOffset(0)
        self.tfb_shadow.setColor(QColor(0, 0, 0, 150))

        self.twofactor_field_animation = QPropertyAnimation(self.twofactor_field_opacity_effect, b"opacity")
        self.twofactor_field_animation.setDuration(500)
        self.twofactor_field_animation.setStartValue(0)
        self.twofactor_field_animation.setEndValue(1)
        self.twofactor_field_animation.setEasingCurve(QEasingCurve.InOutQuart)
        self.twofactor_field_animation.finished.connect(lambda: self.ui.twofactor_field.setFocus())
        self.twofactor_field_animation.finished.connect(
            lambda: self.ui.twofactor_field.setGraphicsEffect(self.tff_shadow))

        self.twofactor_button_animation = QPropertyAnimation(self.twofactor_button_opacity_effect, b"opacity")
        self.twofactor_button_animation.setDuration(500)
        self.twofactor_button_animation.setStartValue(0)
        self.twofactor_button_animation.setEndValue(1)
        self.twofactor_button_animation.setEasingCurve(QEasingCurve.InOutQuart)
        self.twofactor_button_animation.finished.connect(
            lambda: self.ui.twofactor_button.setGraphicsEffect(self.tfb_shadow))

        self.ui.twofactor_button.hide()
        self.ui.twofactor_field.hide()

        self.ui.twofactor_button.clicked.connect(self.buttonClick)

        self.ui.username.returnPressed.connect(self.ui.login_button.click)
        self.ui.password.returnPressed.connect(self.ui.login_button.click)

        self.ui.twofactor_field.returnPressed.connect(self.ui.twofactor_button.click)

        self.fadeInAnimation = QPropertyAnimation(self, b"windowOpacity")
        self.fadeInAnimation.setDuration(350)
        self.fadeInAnimation.setStartValue(0)
        self.fadeInAnimation.setEndValue(1)
        self.fadeInAnimation.setEasingCurve(QEasingCurve.InOutQuart)
        self.fadeInAnimation.start()

        self.ui.ctx_btns.hide()
        for child in self.ui.ctx_btns.children():
            child.hide()
        self.ctx_btns_state = False

        self.ui.btn_dropdown.clicked.connect(self.buttonClick)

    def updateEverything(self):
        self.repaint()
        QApplication.processEvents()

    def stopAnimations(self):
        if self.response_label_animation.state() == QAbstractAnimation.Running:
            self.response_label_animation.stop()
            self.response_label_animation.setCurrentTime(0)  # Reset the animation to the beginning

        if self.response_label_animation_reverse.state() == QAbstractAnimation.Running:
            self.response_label_animation_reverse.stop()
            self.response_label_animation_reverse.setCurrentTime(0)  # Reset the reverse animation to the beginning

        if self.twofactor_responselabel_animation.state() == QAbstractAnimation.Running:
            self.twofactor_responselabel_animation.stop()
            self.twofactor_responselabel_animation.setCurrentTime(0)

        if self.twofactor_responselabel_reverse.state() == QAbstractAnimation.Running:
            self.twofactor_responselabel_reverse.stop()
            self.twofactor_responselabel_reverse.setCurrentTime(0)

        try:
            if self.timer is not None:
                self.timer.stop()
                self.timer.deleteLater()  # Delete the timer if it's no longer needed
                self.timer = None
        except AttributeError:
            pass

    def fadein(self):
        for i in range(0, 101):
            self.setWindowOpacity(i / 100)
            time.sleep(0.01)
            self.updateEverything()

    def fadeInChildren(self):
        def children_animations():
            self.ui.btn_close.show()
            self.ui.btn_minimize.show()

        # If any of the animations are running, stop them
        try:
            if self.fadeInAnimation.state() == QAbstractAnimation.Running:
                self.fadeInAnimation.stop()
                self.fadeInAnimation.setCurrentTime(0)

        except AttributeError:
            pass
        self.ui.ctx_btns.show()
        self.dropdown_geometry_animation = QPropertyAnimation(self.ui.ctx_btns, b"geometry")
        self.dropdown_geometry_animation.setDuration(500)
        # Start at (1232, 0, 0, 0), and extend to (1071, 20, 161, 161)
        self.dropdown_geometry_animation.setStartValue(QRect(326, 15, 0, 0))
        self.dropdown_geometry_animation.setEndValue(QRect(230, 10, 111, 31))
        self.dropdown_geometry_animation.setEasingCurve(QEasingCurve.InOutQuart)
        self.dropdown_geometry_animation.start()
        self.dropdown_geometry_animation.finished.connect(lambda: children_animations())

    def fadeOutChildren(self):
        def children_animations():
            for child in self.ui.ctx_btns.children():
                child.hide()

        children_animations()
        try:
            if self.dropdown_geometry_animation_reverse.state() == QAbstractAnimation.Running:
                self.dropdown_geometry_animation_reverse.stop()
                self.dropdown_geometry_animation_reverse.setCurrentTime(0)
        except AttributeError:
            pass

        self.dropdown_geometry_animation_reverse = QPropertyAnimation(self.ui.ctx_btns, b"geometry")
        self.dropdown_geometry_animation_reverse.setDuration(500)
        # Start at (1071, 20, 161, 161), and extend to (1232, 0, 0, 0)
        self.dropdown_geometry_animation_reverse.setStartValue(QRect(230, 10, 111, 31))
        self.dropdown_geometry_animation_reverse.setEndValue(QRect(326, 15, 0, 0))
        self.dropdown_geometry_animation_reverse.setEasingCurve(QEasingCurve.InOutQuart)
        self.dropdown_geometry_animation_reverse.start()

    # BUTTONS CLICK
    # Post here your functions for clicked buttons
    # ///////////////////////////////////////////////////////////////
    def buttonClick(self):
        # GET BUTTON CLICKED
        btn = self.sender()
        btnName = btn.objectName()
        # SHOW HOME PAGE

        if btnName == "login_button":
            username = self.ui.username.text()
            password = self.ui.password.text()
            if username == "" or password == "":
                self.ui.responseLabel.setText("Please fill in all fields.")
                self.ui.responseLabel.setStyleSheet(
                    "background-color: #d62e2b; color: rgb(255, 255, 255); border-radius: 10px; font: 400 10pt \"Inter Medium\";")
                # Start: X = 0, Y = 440, Width = 321, Height = 0
                # End: X = 0, Y = 370, Width = 321, Height = 41
                # If the animation is already running, stop it
                self.stopAnimations()
                self.response_label_animation.start()
                self.timer = QTimer(self)
                self.timer.singleShot(1000, lambda: self.response_label_animation_reverse.start())
            else:
                login_response, code = login(username, password)
                if code == 200:
                    response, code = device_token(username, password)
                    with open(os.getcwd() + "/config/config.json", "r") as f:
                        try:
                            config = json.load(f)
                        except json.decoder.JSONDecodeError:
                            config = {}
                        f.close()
                    config["username"] = username
                    if isinstance(response, str):
                        response = json.loads(response)
                    config["token"] = response["token"]
                    print(config)
                    with open(os.getcwd() + "/config/config.json", "w") as f:
                        json.dump(config, f)
                        f.close()
                    self.ui.responseLabel.setText("Login successful.")
                    self.ui.responseLabel.setStyleSheet(
                        "background-color: #2abd42; color: rgb(255, 255, 255); border-radius: 10px; font: 400 10pt \"Inter Medium\";")
                    self.stopAnimations()
                    self.response_label_animation.start()
                    self.timer = QTimer(self)
                    self.timer.singleShot(1000, lambda: self.successfulLogin(login_response))
                elif "2FA" in login_response["detail"]:
                    # Change to the twofactor page
                    self.__cached_username = username
                    self.__cached_password = password
                    self.ui.pages.setCurrentWidget(self.ui.twofactor)
                    self.ui.twofactor_responselabel.setText(login_response["detail"])
                    self.ui.twofactor_responselabel.setStyleSheet(
                        "background-color: #d62e2b; color: rgb(255, 255, 255); border-radius: 10px; font: 400 10pt \"Inter Medium\";")
                    self.stopAnimations()
                    self.twofactor_responselabel_animation.start()
                    self.timer = QTimer(self)
                    self.timer.singleShot(1000, lambda: self.twofactor_responselabel_reverse.start())
                    self.ui.twofactor_field.show()
                    self.ui.twofactor_button.show()
                    self.twofactor_field_animation.start()
                    self.twofactor_button_animation.start()
                else:
                    self.ui.responseLabel.setText(login_response["detail"])
                    self.ui.responseLabel.setStyleSheet(
                        "background-color: #d62e2b; color: rgb(255, 255, 255); border-radius: 10px; font: 400 10pt \"Inter Medium\";")
                    self.stopAnimations()
                    self.response_label_animation.start()
                    self.timer = QTimer(self)
                    self.timer.singleShot(1000, lambda: self.response_label_animation_reverse.start())

        elif btnName == "register_button":
            webbrowser.get().open("https://ameasere.com/sign-up.html")

        elif btnName == "btn_dropdown":
            if self.ctx_btns_state:
                self.ctx_btns_state = False
                self.fadeOutChildren()
                self.ui.btn_dropdown.setIcon(QIcon(":/icons/images/icons/arrow-down-left.png"))
            else:
                self.ui.ctx_btns.show()
                self.ctx_btns_state = True
                self.fadeInChildren()
                self.ui.btn_dropdown.setIcon(QIcon(":/icons/images/icons/arrow-up-right.png"))

        elif btnName == "twofactor_button":
            response, code = two_factor(self.__cached_username, self.__cached_password, self.ui.twofactor_field.text())
            if code == 200:
                with open(os.getcwd() + "/config/config.json", "r") as f:
                    try:
                        config = json.load(f)
                    except json.decoder.JSONDecodeError:
                        config = {}
                    f.close()
                    if isinstance(response, str):
                        response = json.loads(response)
                rt = response["2fa_rt"]
                response, code = device_token(self.__cached_username, self.__cached_password, rt=rt)
                if code == 200:
                    if isinstance(response, str):
                        response = json.loads(response)
                    config["username"] = self.__cached_username
                    if isinstance(response, str):
                        response = json.loads(response)
                    config["token"] = response["token"]
                    print(config)
                    with open(os.getcwd() + "/config/config.json", "w") as f:
                        json.dump(config, f)
                        f.close()
                    response, code = token_login(self.__cached_password, config["token"])
                    self.ui.twofactor_responselabel.setText("Login successful.")
                    self.ui.twofactor_responselabel.setStyleSheet(
                        "background-color: #2abd42; color: rgb(255, 255, 255); border-radius: 10px; font: 400 10pt \"Inter Medium\";")
                    self.stopAnimations()
                    self.twofactor_responselabel_animation.start()
                    self.timer = QTimer(self)
                    self.timer.singleShot(1000, lambda: self.successfulLogin(response))
            else:
                self.ui.twofactor_responselabel.setText(response["detail"])
                self.ui.twofactor_responselabel.setStyleSheet(
                    "background-color: #d62e2b; color: rgb(255, 255, 255); border-radius: 10px; font: 400 10pt \"Inter Medium\";")
                self.stopAnimations()
                self.twofactor_responselabel_animation.start()
                self.timer = QTimer(self)
                self.timer.singleShot(1000, lambda: self.twofactor_responselabel_reverse.start())


    def openMainWindow(self, response):
        self.mainWindow = MainWindow(response)
        self.mainWindow.show()
        self.close()

    def successfulLogin(self, response):
        def mainWindowOpener():
            # Fade out animation
            self.fadeOutAnimation = QPropertyAnimation(self, b"windowOpacity")
            self.fadeOutAnimation.setDuration(350)
            self.fadeOutAnimation.setStartValue(1)
            self.fadeOutAnimation.setEndValue(0)
            self.fadeOutAnimation.setEasingCurve(QEasingCurve.InOutQuart)
            # Start after a QTimer of 1 second
            self.timer = QTimer(self)
            self.timer.singleShot(700, lambda: self.fadeOutAnimation.start())
            self.fadeOutAnimation.finished.connect(lambda: self.openMainWindow(response))

        if self.ui.pages.currentWidget() == self.ui.login:
            self.response_label_animation_reverse.start()
            self.response_label_animation_reverse.finished.connect(lambda: mainWindowOpener())
        elif self.ui.pages.currentWidget() == self.ui.twofactor:
            self.twofactor_responselabel_reverse.start()
            self.twofactor_responselabel_reverse.finished.connect(lambda: mainWindowOpener())

    # MOUSE CLICK EVENTS
    # ///////////////////////////////////////////////////////////////
    def mousePressEvent(self, event):
        # SET DRAG POS WINDOW
        self.dragPos = event.globalPosition().toPoint()


class TokenLoginWindow(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        # SET AS GLOBAL WIDGETS
        # ///////////////////////////////////////////////////////////////
        self.dragPos = None
        self.ui = Ui_TokenLoginWindow()
        self.ui.setupUi(self)
        widgets = self.ui

        # USE CUSTOM TITLE BAR | USE AS "False" FOR MAC OR LINUX
        # ///////////////////////////////////////////////////////////////
        Settings.ENABLE_CUSTOM_TITLE_BAR = True
        if not Settings.ENABLE_CUSTOM_TITLE_BAR:
            widgets.bgApp.setStyleSheet("border-top-left-radius: 0px; border-top-right-radius: 0px;")
            self.ui.appMargins.setContentsMargins(0, 0, 0, 0)
            self.ui.btn_minimize.hide()
            self.ui.btn_close.hide()
        else:
            # STANDARD TITLE BAR
            self.setWindowFlags(Qt.FramelessWindowHint)
            self.setAttribute(Qt.WA_TranslucentBackground)

            # MOVE WINDOW / MAXIMIZE / RESTORE
            def moveWindow(event):
                # MOVE WINDOW
                if event.buttons() == Qt.LeftButton:
                    self.move(self.pos() + event.globalPosition().toPoint() - self.dragPos)
                    self.dragPos = event.globalPosition().toPoint()
                    event.accept()

            self.ui.dragBar.mouseMoveEvent = moveWindow
        self.shadow = QGraphicsDropShadowEffect(self)
        self.shadow.setBlurRadius(17)
        self.shadow.setXOffset(0)
        self.shadow.setYOffset(0)
        self.shadow.setColor(QColor(0, 0, 0, 150))
        self.ui.bgApp.setGraphicsEffect(self.shadow)
        self.ui.btn_minimize.clicked.connect(lambda: self.showMinimized())

        self.fadeInAnimation = QPropertyAnimation(self, b"windowOpacity")
        self.fadeInAnimation.setDuration(350)
        self.fadeInAnimation.setStartValue(0)
        self.fadeInAnimation.setEndValue(1)
        self.fadeInAnimation.setEasingCurve(QEasingCurve.InOutQuart)
        self.fadeInAnimation.start()

        self.backgroundAnimation = QPropertyAnimation(self.ui.bg1, b"geometry")
        self.backgroundAnimation.setDuration(800)
        self.backgroundAnimation.setStartValue(QRect(0, 0, 31, 501))
        self.backgroundAnimation.setEndValue(QRect(0, 0, 310, 501))
        self.backgroundAnimation.setEasingCurve(QEasingCurve.InOutQuart)
        self.backgroundAnimation.start()

        # CLOSE APPLICATION
        self.ui.btn_close.clicked.connect(lambda: self.close())

        # APP NAME
        # ///////////////////////////////////////////////////////////////
        title = "Polaris"
        # APPLY TEXTS
        self.setWindowTitle(title)

        self.ui.passwordLabel.hide()
        self.ui.password.hide()

        # LEFT MENUS
        widgets.loginNormalButton.clicked.connect(self.buttonClick)
        widgets.loginTokenButton.clicked.connect(self.buttonClick)
        widgets.btn_dropdown.clicked.connect(self.buttonClick)

        # widgets.settingsTopBtn.hide()

        self.paintEvent(None)

        # If enter key is pressed while focus is on the password field, click the login button
        self.ui.password.returnPressed.connect(self.ui.loginTokenButton.click)

        # SHOW APP
        # ///////////////////////////////////////////////////////////////
        self.show()

        # SET HOME PAGE AND SELECT MENU
        # ///////////////////////////////////////////////////////////////
        self.ui.pages.setCurrentWidget(self.ui.login)

        self.password_label_opacity_effect = QGraphicsOpacityEffect(self.ui.passwordLabel)
        self.ui.passwordLabel.setGraphicsEffect(self.password_label_opacity_effect)
        self.password_label_opacity_effect.setOpacity(0)

        self.passwordLabelAnimation = QPropertyAnimation(self.password_label_opacity_effect, b"opacity")
        self.passwordLabelAnimation.setDuration(500)
        self.passwordLabelAnimation.setStartValue(0)
        self.passwordLabelAnimation.setEndValue(1)
        self.passwordLabelAnimation.setEasingCurve(QEasingCurve.InOutQuart)
        self.passwordLabelAnimation.finished.connect(lambda: self.ui.passwordLabel.setGraphicsEffect(None))
        self.passwordLabelAnimation.start()
        self.ui.passwordLabel.show()

        self.password_opacity_effect = QGraphicsOpacityEffect(self.ui.password)
        self.ui.password.setGraphicsEffect(self.password_opacity_effect)
        self.password_opacity_effect.setOpacity(0)

        self.password_shadow = QGraphicsDropShadowEffect(self.ui.password)
        self.password_shadow.setBlurRadius(17)
        self.password_shadow.setXOffset(0)
        self.password_shadow.setYOffset(0)
        self.password_shadow.setColor(QColor(0, 0, 0, 150))

        self.passwordAnimation = QPropertyAnimation(self.password_opacity_effect, b"opacity")
        self.passwordAnimation.setDuration(500)
        self.passwordAnimation.setStartValue(0)
        self.passwordAnimation.setEndValue(1)
        self.passwordAnimation.setEasingCurve(QEasingCurve.InOutQuart)
        self.passwordAnimation.finished.connect(lambda: self.ui.password.setGraphicsEffect(self.password_shadow))
        self.passwordAnimation.start()
        self.ui.password.show()

        self.response_label_animation = QPropertyAnimation(self.ui.responseLabel, b"geometry")
        self.response_label_animation.setDuration(500)
        self.response_label_animation.setStartValue(QRect(0, 511, 351, 0))
        self.response_label_animation.setEndValue(QRect(0, 460, 351, 41))
        self.response_label_animation.setEasingCurve(QEasingCurve.InOutQuart)

        self.response_label_animation_reverse = QPropertyAnimation(self.ui.responseLabel, b"geometry")
        self.response_label_animation_reverse.setDuration(500)
        self.response_label_animation_reverse.setStartValue(QRect(0, 460, 351, 41))
        self.response_label_animation_reverse.setEndValue(QRect(0, 511, 351, 0))
        self.response_label_animation_reverse.setEasingCurve(QEasingCurve.InOutQuart)

        self.ui.ctx_btns.hide()
        for child in self.ui.ctx_btns.children():
            child.hide()
        self.ctx_btns_state = False

    def fadein(self):
        for i in range(0, 101):
            self.setWindowOpacity(i / 100)
            time.sleep(0.01)
            QApplication.processEvents()

    def stopAnimations(self):
        if self.response_label_animation.state() == QAbstractAnimation.Running:
            self.response_label_animation.stop()
            self.response_label_animation.setCurrentTime(0)  # Reset the animation to the beginning

        if self.response_label_animation_reverse.state() == QAbstractAnimation.Running:
            self.response_label_animation_reverse.stop()
            self.response_label_animation_reverse.setCurrentTime(0)  # Reset the reverse animation to the beginning
        try:
            if self.timer is not None:
                self.timer.stop()
                self.timer.deleteLater()  # Delete the timer if it's no longer needed
                self.timer = None
        except AttributeError:
            pass

    # BUTTONS CLICK
    # Post here your functions for clicked buttons
    # ///////////////////////////////////////////////////////////////
    def buttonClick(self):
        # GET BUTTON CLICKED
        btn = self.sender()
        btnName = btn.objectName()
        # SHOW HOME PAGE

        if btnName == "loginNormalButton":
            loginNormalWindow = FirstRunWindow()
            loginNormalWindow.show()
            self.fadeOutAnimation = QPropertyAnimation(self, b"windowOpacity")
            self.fadeOutAnimation.setDuration(350)
            self.fadeOutAnimation.setStartValue(1)
            self.fadeOutAnimation.setEndValue(0)
            self.fadeOutAnimation.setEasingCurve(QEasingCurve.InOutQuart)
            # Start after a QTimer of 1 second
            self.timer = QTimer(self)
            self.timer.singleShot(700, lambda: self.fadeOutAnimation.start())
            self.fadeOutAnimation.finished.connect(lambda: self.close())

        elif btnName == "loginTokenButton":
            password = self.ui.password.text()
            if password == "":
                self.ui.responseLabel.setText("Please fill in all fields.")
                self.ui.responseLabel.setStyleSheet(
                    "background-color: #d62e2b; color: rgb(255, 255, 255); border-radius: 10px; font: 400 10pt \"Inter Medium\";")
                # Start: X = 0, Y = 440, Width = 321, Height = 0
                # End: X = 0, Y = 370, Width = 321, Height = 41
                # If the animation is already running, stop it
                self.stopAnimations()
                self.response_label_animation.start()
                self.timer = QTimer(self)
                self.timer.singleShot(1000, lambda: self.response_label_animation_reverse.start())
            else:
                with open(os.getcwd() + "/config/config.json", "r") as f:
                    config = json.load(f)
                    f.close()
                token = config["token"]
                response, code = token_login(password, token)
                if code == 200:
                    self.ui.responseLabel.setText("Login successful.")
                    self.ui.responseLabel.setStyleSheet(
                        "background-color: #2abd42; color: rgb(255, 255, 255); border-radius: 10px; font: 400 10pt \"Inter Medium\";")
                    self.stopAnimations()
                    self.response_label_animation.start()
                    self.timer = QTimer(self)
                    self.timer.singleShot(1000, lambda: self.successfulLogin(response))
                else:
                    self.ui.responseLabel.setText("Please log in normally to reset your token.")
                    config["token"] = ""
                    config["username"] = ""
                    with open(os.getcwd() + "/config/config.json", "w") as f:
                        json.dump(config, f)
                        f.close()
                    self.ui.responseLabel.setStyleSheet(
                        "background-color: #d62e2b; color: rgb(255, 255, 255); border-radius: 10px; font: 400 10pt \"Inter Medium\";")
                    self.stopAnimations()
                    self.response_label_animation.start()
                    self.timer = QTimer(self)
                    self.timer.singleShot(1000, lambda: self.response_label_animation_reverse.start())

        elif btnName == "btn_dropdown":
            if self.ctx_btns_state:
                self.ctx_btns_state = False
                self.fadeOutChildren()
                self.ui.btn_dropdown.setIcon(QIcon(":/icons/images/icons/arrow-down-left.png"))
            else:
                self.ui.ctx_btns.show()
                self.ctx_btns_state = True
                self.fadeInChildren()
                self.ui.btn_dropdown.setIcon(QIcon(":/icons/images/icons/arrow-up-right.png"))

    def openMainWindow(self, response):
        self.mainWindow = MainWindow(response)
        self.mainWindow.show()
        self.close()

    def fadeInChildren(self):
        def children_animations():
            self.ui.btn_close.show()
            self.ui.btn_minimize.show()

        # If any of the animations are running, stop them
        try:
            if self.fadeInAnimation.state() == QAbstractAnimation.Running:
                self.fadeInAnimation.stop()
                self.fadeInAnimation.setCurrentTime(0)

        except AttributeError:
            pass
        self.ui.ctx_btns.show()
        self.dropdown_geometry_animation = QPropertyAnimation(self.ui.ctx_btns, b"geometry")
        self.dropdown_geometry_animation.setDuration(500)
        # Start at (1232, 0, 0, 0), and extend to (1071, 20, 161, 161)
        self.dropdown_geometry_animation.setStartValue(QRect(326, 15, 0, 0))
        self.dropdown_geometry_animation.setEndValue(QRect(230, 10, 111, 31))
        self.dropdown_geometry_animation.setEasingCurve(QEasingCurve.InOutQuart)
        self.dropdown_geometry_animation.start()
        self.dropdown_geometry_animation.finished.connect(lambda: children_animations())

    def fadeOutChildren(self):
        def children_animations():
            for child in self.ui.ctx_btns.children():
                child.hide()

        children_animations()
        try:
            if self.dropdown_geometry_animation_reverse.state() == QAbstractAnimation.Running:
                self.dropdown_geometry_animation_reverse.stop()
                self.dropdown_geometry_animation_reverse.setCurrentTime(0)
        except AttributeError:
            pass

        self.dropdown_geometry_animation_reverse = QPropertyAnimation(self.ui.ctx_btns, b"geometry")
        self.dropdown_geometry_animation_reverse.setDuration(500)
        # Start at (1071, 20, 161, 161), and extend to (1232, 0, 0, 0)
        self.dropdown_geometry_animation_reverse.setStartValue(QRect(230, 10, 111, 31))
        self.dropdown_geometry_animation_reverse.setEndValue(QRect(326, 15, 0, 0))
        self.dropdown_geometry_animation_reverse.setEasingCurve(QEasingCurve.InOutQuart)
        self.dropdown_geometry_animation_reverse.start()

    def successfulLogin(self, response):
        def mainWindowOpener():
            # Fade out animation
            self.fadeOutAnimation = QPropertyAnimation(self, b"windowOpacity")
            self.fadeOutAnimation.setDuration(350)
            self.fadeOutAnimation.setStartValue(1)
            self.fadeOutAnimation.setEndValue(0)
            self.fadeOutAnimation.setEasingCurve(QEasingCurve.InOutQuart)
            # Start after a QTimer of 1 second
            self.timer = QTimer(self)
            self.timer.singleShot(700, lambda: self.fadeOutAnimation.start())
            self.fadeOutAnimation.finished.connect(lambda: self.openMainWindow(response))

        self.response_label_animation_reverse.start()
        self.response_label_animation_reverse.finished.connect(lambda: mainWindowOpener())

    # MOUSE CLICK EVENTS
    # ///////////////////////////////////////////////////////////////
    def mousePressEvent(self, event):
        # SET DRAG POS WINDOW
        self.dragPos = event.globalPosition().toPoint()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon("icon.ico"))
    config = preliminary_config_check()
    if "token" not in config or config["token"] == "":
        window = FirstRunWindow()
    else:
        window = TokenLoginWindow()
    sys.exit(app.exec())
