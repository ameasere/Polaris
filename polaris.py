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
        self.ui.extraLabel.setText(self.__response["username"])

        # TOGGLE MENU
        # ///////////////////////////////////////////////////////////////
        self.ui.toggleButton.clicked.connect(lambda: UIFunctions.toggleMenu(self, True))

        # SET UI DEFINITIONS
        # ///////////////////////////////////////////////////////////////
        UIFunctions.uiDefinitions(self)

        # QTableWidget PARAMETERS
        # ///////////////////////////////////////////////////////////////
        self.ui.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        # BUTTONS CLICK
        # ///////////////////////////////////////////////////////////////

        # LEFT MENUS
        self.ui.btn_home.clicked.connect(self.buttonClick)
        self.ui.btn_widgets.clicked.connect(self.buttonClick)
        self.ui.btn_new.clicked.connect(self.buttonClick)
        self.ui.btn_save.clicked.connect(self.buttonClick)

        # widgets.settingsTopBtn.hide()

        # EXTRA LEFT BOX
        def openCloseLeftBox():
            UIFunctions.toggleLeftBox(self, True)

        self.ui.toggleLeftBox.clicked.connect(openCloseLeftBox)
        self.ui.extraCloseColumnBtn.clicked.connect(openCloseLeftBox)

        self.paintEvent(None)

        if "stafficon" in self.__response:
            icon = self.__response["stafficon"].encode("utf-8")
            # Set it as the background image for extraIcon
            self.ui.extraIcon.setStyleSheet("background-position: center; background-repeat: no-repeat;")
            # Write the image to a file in the temp folder, and set in stylesheet dynamically
            with open(os.getcwd() + "/temp/icon.png", "wb") as f:
                f.write(base64.b64decode(icon))
                f.close()
            path = os.getcwd() + "/temp/icon.png"
            path = path.replace("\\", "/")
            self.ui.extraIcon.setStyleSheet(self.ui.extraIcon.styleSheet() + f" background-image: url({path});")
        # If the subscription JSON object is not empty
        elif "icon" in self.__response["subscription"]:
            icon = self.__response["subscription"]["icon"].encode("utf-8")
            with open(os.getcwd() + "/temp/icon.png", "wb") as f:
                f.write(base64.b64decode(icon))
                f.close()
            path = os.getcwd() + "/temp/icon.png"
            path = path.replace("\\", "/")
            self.ui.extraIcon.setStyleSheet(self.ui.extraIcon.styleSheet() + f" background-image: url({path});")
        else:
            self.ui.extraIcon.setStyleSheet(
                "background-position: center; background-repeat: no-repeat; background-image: url(\":/icons/images/icons/user.png\");")

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
        self.ui.stackedWidget.setCurrentWidget(self.ui.home)
        self.ui.btn_home.setStyleSheet(UIFunctions.selectMenu(self.ui.btn_home.styleSheet()))
        self.current_page = "home"
        # If the current page is "home", then change the button background image
        self.ui.btn_home.setStyleSheet(
            self.ui.btn_home.styleSheet() + "background-image: url(\":/icons/images/icons/home_selected.png\");")

    # BUTTONS CLICK
    # Post here your functions for clicked buttons
    # ///////////////////////////////////////////////////////////////
    def buttonClick(self):
        # GET BUTTON CLICKED
        btn = self.sender()
        btnName = btn.objectName()

        # SHOW HOME PAGE
        if btnName == "btn_home":
            self.ui.stackedWidget.setCurrentWidget(self.ui.home)
            UIFunctions.resetStyle(self, btnName)
            btn.setStyleSheet(UIFunctions.selectMenu(
                btn.styleSheet()) + "background-image: url(\":/icons/images/icons/home_selected.png\");")
            self.current_page = "home"

        # SHOW WIDGETS PAGE
        if btnName == "btn_widgets":
            self.ui.stackedWidget.setCurrentWidget(self.ui.widgets)
            UIFunctions.resetStyle(self, btnName)
            btn.setStyleSheet(UIFunctions.selectMenu(btn.styleSheet()))
            self.current_page = "widgets"
            # Replace the background image of the button
            self.ui.btn_home.setStyleSheet(
                self.ui.btn_home.styleSheet() + "background-image: url(\":/icons/images/icons/home_unselected.png\");")

        # SHOW NEW PAGE
        if btnName == "btn_new":
            self.ui.stackedWidget.setCurrentWidget(self.ui.new_page)  # SET PAGE
            UIFunctions.resetStyle(self, btnName)  # RESET ANOTHERS BUTTONS SELECTED
            btn.setStyleSheet(UIFunctions.selectMenu(btn.styleSheet()))  # SELECT MENU
            self.current_page = "new"
            # Replace the background image of the button
            self.ui.btn_home.setStyleSheet(
                self.ui.btn_home.styleSheet() + "background-image: url(\":/icons/images/icons/home_unselected.png\");")

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


class FirstRunWindow(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        # SET AS GLOBAL WIDGETS
        # ///////////////////////////////////////////////////////////////
        self.dragPos = None
        self.ui = Ui_FirstRunWindow()
        self.ui.setupUi(self)
        widgets = self.ui
        titleBarEnabled = True if platform.system() == "Windows" else False
        # USE CUSTOM TITLE BAR | USE AS "False" FOR MAC OR LINUX
        # ///////////////////////////////////////////////////////////////
        Settings.ENABLE_CUSTOM_TITLE_BAR = titleBarEnabled
        if not Settings.ENABLE_CUSTOM_TITLE_BAR:
            widgets.bgApp.setStyleSheet("border-top-left-radius: 0px; border-top-right-radius: 0px;")
            self.ui.appMargins.setContentsMargins(0, 0, 0, 0)
            self.ui.minimizeAppBtn.hide()
            self.ui.closeAppBtn.hide()
        else:
            # STANDARD TITLE BAR
            self.setWindowFlags(Qt.FramelessWindowHint)
            self.setAttribute(Qt.WA_TranslucentBackground)

            # MOVE WINDOW / MAXIMIZE / RESTORE
            def moveWindow(event):
                # IF MAXIMIZED CHANGE TO NORMAL
                if UIFunctions.returStatus(self):
                    UIFunctions.maximize_restore(self)
                # MOVE WINDOW
                if event.buttons() == Qt.LeftButton:
                    self.move(self.pos() + event.globalPosition().toPoint() - self.dragPos)
                    self.dragPos = event.globalPosition().toPoint()
                    event.accept()

            self.ui.titleLeftDescription.mouseMoveEvent = moveWindow
        self.shadow = QGraphicsDropShadowEffect(self)
        self.shadow.setBlurRadius(17)
        self.shadow.setXOffset(0)
        self.shadow.setYOffset(0)
        self.shadow.setColor(QColor(0, 0, 0, 150))
        self.ui.bgApp.setGraphicsEffect(self.shadow)
        self.ui.minimizeAppBtn.clicked.connect(lambda: self.showMinimized())

        # CLOSE APPLICATION
        self.ui.closeAppBtn.clicked.connect(lambda: self.close())

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
        widgets.stackedWidget.setCurrentWidget(widgets.login)

        self.titleShadow = QGraphicsDropShadowEffect(self.ui.motto_2)
        self.titleShadow.setBlurRadius(17)
        self.titleShadow.setXOffset(0)
        self.titleShadow.setYOffset(0)
        self.titleShadow.setColor(QColor(0, 0, 0, 150))
        self.ui.motto_2.setGraphicsEffect(self.titleShadow)

        self.titleShadow2 = QGraphicsDropShadowEffect(self.ui.welcome)
        self.titleShadow2.setBlurRadius(17)
        self.titleShadow2.setXOffset(0)
        self.titleShadow2.setYOffset(0)
        self.titleShadow2.setColor(QColor(0, 0, 0, 150))
        self.ui.welcome.setGraphicsEffect(self.titleShadow2)

        self.titleShadow3 = QGraphicsDropShadowEffect(self.ui.motto)
        self.titleShadow3.setBlurRadius(17)
        self.titleShadow3.setXOffset(0)
        self.titleShadow3.setYOffset(0)
        self.titleShadow3.setColor(QColor(0, 0, 0, 150))
        self.ui.motto.setGraphicsEffect(self.titleShadow3)

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
        self.response_label_animation.setStartValue(QRect(0, 440, 321, 0))
        self.response_label_animation.setEndValue(QRect(0, 380, 321, 30))
        self.response_label_animation.setEasingCurve(QEasingCurve.InBounce)

        self.response_label_animation_reverse = QPropertyAnimation(self.ui.responseLabel, b"geometry")
        self.response_label_animation_reverse.setDuration(500)
        self.response_label_animation_reverse.setStartValue(QRect(0, 380, 321, 30))
        self.response_label_animation_reverse.setEndValue(QRect(0, 440, 321, 0))
        self.response_label_animation_reverse.setEasingCurve(QEasingCurve.OutBounce)
        self.response_label_animation_reverse.finished.connect(lambda: self.updateEverything)

        self.twofactor_responselabel_animation = QPropertyAnimation(self.ui.twofactor_responselabel, b"geometry")
        self.twofactor_responselabel_animation.setDuration(500)
        self.twofactor_responselabel_animation.setStartValue(QRect(0, 440, 321, 0))
        self.twofactor_responselabel_animation.setEndValue(QRect(0, 380, 321, 30))
        self.twofactor_responselabel_animation.setEasingCurve(QEasingCurve.InBounce)

        self.twofactor_responselabel_reverse = QPropertyAnimation(self.ui.twofactor_responselabel, b"geometry")
        self.twofactor_responselabel_reverse.setDuration(500)
        self.twofactor_responselabel_reverse.setStartValue(QRect(0, 380, 321, 30))
        self.twofactor_responselabel_reverse.setEndValue(QRect(0, 440, 321, 0))
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
        self.twofactor_field_animation.finished.connect(lambda: self.ui.twofactor_field.setGraphicsEffect(self.tff_shadow))

        self.twofactor_button_animation = QPropertyAnimation(self.twofactor_button_opacity_effect, b"opacity")
        self.twofactor_button_animation.setDuration(500)
        self.twofactor_button_animation.setStartValue(0)
        self.twofactor_button_animation.setEndValue(1)
        self.twofactor_button_animation.setEasingCurve(QEasingCurve.InOutQuart)
        self.twofactor_button_animation.finished.connect(lambda: self.ui.twofactor_button.setGraphicsEffect(self.tfb_shadow))

        self.ui.twofactor_button.hide()
        self.ui.twofactor_field.hide()

        self.ui.twofactor_button.clicked.connect(self.buttonClick)


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
                    self.ui.stackedWidget.setCurrentWidget(self.ui.twofactor)
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

        if self.ui.stackedWidget.currentWidget() == self.ui.login:
            self.response_label_animation_reverse.start()
            self.response_label_animation_reverse.finished.connect(lambda: mainWindowOpener())
        elif self.ui.stackedWidget.currentWidget() == self.ui.twofactor:
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
        titleBarEnabled = True if platform.system() == "Windows" else False
        # USE CUSTOM TITLE BAR | USE AS "False" FOR MAC OR LINUX
        # ///////////////////////////////////////////////////////////////
        Settings.ENABLE_CUSTOM_TITLE_BAR = titleBarEnabled
        if not Settings.ENABLE_CUSTOM_TITLE_BAR:
            widgets.bgApp.setStyleSheet("border-top-left-radius: 0px; border-top-right-radius: 0px;")
            self.ui.appMargins.setContentsMargins(0, 0, 0, 0)
            self.ui.minimizeAppBtn.hide()
            self.ui.closeAppBtn.hide()
        else:
            # STANDARD TITLE BAR
            self.setWindowFlags(Qt.FramelessWindowHint)
            self.setAttribute(Qt.WA_TranslucentBackground)

            # MOVE WINDOW / MAXIMIZE / RESTORE
            def moveWindow(event):
                # IF MAXIMIZED CHANGE TO NORMAL
                if UIFunctions.returStatus(self):
                    UIFunctions.maximize_restore(self)
                # MOVE WINDOW
                if event.buttons() == Qt.LeftButton:
                    self.move(self.pos() + event.globalPosition().toPoint() - self.dragPos)
                    self.dragPos = event.globalPosition().toPoint()
                    event.accept()

            self.ui.titleLeftDescription.mouseMoveEvent = moveWindow
        self.shadow = QGraphicsDropShadowEffect(self)
        self.shadow.setBlurRadius(17)
        self.shadow.setXOffset(0)
        self.shadow.setYOffset(0)
        self.shadow.setColor(QColor(0, 0, 0, 150))
        self.ui.bgApp.setGraphicsEffect(self.shadow)
        self.ui.minimizeAppBtn.clicked.connect(lambda: self.showMinimized())

        self.titleShadow4 = QGraphicsDropShadowEffect(self.ui.motto_2)
        self.titleShadow4.setBlurRadius(17)
        self.titleShadow4.setXOffset(0)
        self.titleShadow4.setYOffset(0)
        self.titleShadow4.setColor(QColor(0, 0, 0, 150))
        self.ui.motto_2.setGraphicsEffect(self.titleShadow4)

        # CLOSE APPLICATION
        self.ui.closeAppBtn.clicked.connect(lambda: self.close())

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

        # widgets.settingsTopBtn.hide()

        self.paintEvent(None)

        # SHOW APP
        # ///////////////////////////////////////////////////////////////
        self.show()

        # SET HOME PAGE AND SELECT MENU
        # ///////////////////////////////////////////////////////////////
        widgets.stackedWidget.setCurrentWidget(widgets.login)

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
        self.response_label_animation.setStartValue(QRect(0, 440, 321, 0))
        self.response_label_animation.setEndValue(QRect(0, 380, 321, 30))
        self.response_label_animation.setEasingCurve(QEasingCurve.InOutQuart)

        self.response_label_animation_reverse = QPropertyAnimation(self.ui.responseLabel, b"geometry")
        self.response_label_animation_reverse.setDuration(500)
        self.response_label_animation_reverse.setStartValue(QRect(0, 380, 321, 30))
        self.response_label_animation_reverse.setEndValue(QRect(0, 440, 321, 0))
        self.response_label_animation_reverse.setEasingCurve(QEasingCurve.InOutQuart)

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
