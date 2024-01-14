from modules import *
from .FirstRunWindow import FirstRunWindow
from .MainWindow import MainWindow

from modules.backend_login import token_login
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

        self.ui.responseLabel.setGeometry(QRect(0, 511, 351, 0))

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
                    "background-color: #001010; color: #e51328; border-radius: 10px; font: 400 10pt \"Inter Medium\"; border: 1px solid #e51328;")
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
                        "background-color: #001010; color: rgb(99, 255, 122); border-radius: 10px; font: 400 10pt \"Inter Medium\"; border: 1px solid rgb(99, 255, 122);")
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
                        "background-color: #001010; color: #e51328; border-radius: 10px; font: 400 10pt \"Inter Medium\"; border: 1px solid #e51328;")
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