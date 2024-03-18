from modules import *
from modules.backend_login import login, device_token, two_factor, token_login
from .MainWindow import MainWindow


class LoginWindow(QMainWindow):
    def __init__(self, window, config):
        QMainWindow.__init__(self)
        # SET AS GLOBAL WIDGETS
        # ///////////////////////////////////////////////////////////////
        self.dragPos = None
        self.ui = Ui_LoginWindow()
        self.ui.setupUi(self)
        self.config = config
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

        self.ui.responseLabel.setGeometry(QRect(0, 511, 351, 0))

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
        widgets.loginNormalButton.clicked.connect(self.buttonClick)
        widgets.loginTokenButton.clicked.connect(self.buttonClick)

        self.ui.password.returnPressed.connect(self.ui.loginTokenButton.click)
        self.ui.password_token.returnPressed.connect(self.ui.loginTokenButton.click)

        # widgets.settingsTopBtn.hide()

        self.paintEvent(None)

        # SHOW APP
        # ///////////////////////////////////////////////////////////////
        self.show()

        # SET HOME PAGE AND SELECT MENU
        # ///////////////////////////////////////////////////////////////
        if window == "password":
            widgets.pages.setCurrentWidget(widgets.password_login)
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
        elif window == "token":
            widgets.pages.setCurrentWidget(widgets.token_login)
            self.password_label_opacity_effect = QGraphicsOpacityEffect(self.ui.passwordLabel_3)
            self.ui.passwordLabel.setGraphicsEffect(self.password_label_opacity_effect)
            self.password_label_opacity_effect.setOpacity(0)

            self.passwordLabelAnimation = QPropertyAnimation(self.password_label_opacity_effect, b"opacity")
            self.passwordLabelAnimation.setDuration(500)
            self.passwordLabelAnimation.setStartValue(0)
            self.passwordLabelAnimation.setEndValue(1)
            self.passwordLabelAnimation.setEasingCurve(QEasingCurve.InOutQuart)
            self.passwordLabelAnimation.finished.connect(lambda: self.ui.passwordLabel_3.setGraphicsEffect(None))
            self.passwordLabelAnimation.start()
            self.ui.passwordLabel.show()

            self.password_opacity_effect = QGraphicsOpacityEffect(self.ui.password_token)
            self.ui.password.setGraphicsEffect(self.password_opacity_effect)
            self.password_opacity_effect.setOpacity(0)

            self.password_shadow = QGraphicsDropShadowEffect(self.ui.password_token)
            self.password_shadow.setBlurRadius(17)
            self.password_shadow.setXOffset(0)
            self.password_shadow.setYOffset(0)
            self.password_shadow.setColor(QColor(0, 0, 0, 150))

            self.passwordAnimation = QPropertyAnimation(self.password_opacity_effect, b"opacity")
            self.passwordAnimation.setDuration(500)
            self.passwordAnimation.setStartValue(0)
            self.passwordAnimation.setEndValue(1)
            self.passwordAnimation.setEasingCurve(QEasingCurve.InOutQuart)
            self.passwordAnimation.finished.connect(
                lambda: self.ui.password_token.setGraphicsEffect(self.password_shadow))
            self.passwordAnimation.start()
            self.ui.password_token.show()

        self.backgroundAnimation = QPropertyAnimation(self.ui.bg1, b"geometry")
        self.backgroundAnimation.setDuration(800)
        self.backgroundAnimation.setStartValue(QRect(0, 0, 31, 501))
        self.backgroundAnimation.setEndValue(QRect(0, 0, 310, 501))
        self.backgroundAnimation.setEasingCurve(QEasingCurve.InOutQuart)
        self.backgroundAnimation.start()

        self.backgroundAnimationReverse = QPropertyAnimation(self.ui.bg1, b"geometry")
        self.backgroundAnimationReverse.setDuration(800)
        self.backgroundAnimationReverse.setStartValue(QRect(0, 0, 310, 501))
        self.backgroundAnimationReverse.setEndValue(QRect(0, 0, 31, 501))
        self.backgroundAnimationReverse.setEasingCurve(QEasingCurve.InOutQuart)

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
                    "background-color: #001010; color: #e51328; border-radius: 10px; font: 600 10pt \"Inter Medium\"; border: 1px solid #e51328;")
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
                        "background-color: #001010; color: #001010; border-radius: 10px; font: 600 10pt \"Inter Medium\"; border: 1px solid rgb(99, 255, 122);")
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
                        "background-color: #001010; color: #e51328; border-radius: 10px; font: 600 10pt \"Inter Medium\"; border: 1px solid #e51328;")
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
                        "background-color: #001010; color: #e51328; border-radius: 10px; font: 600 10pt \"Inter Medium\"; border: 1px solid #e51328;")
                    self.stopAnimations()
                    self.response_label_animation.start()
                    self.timer = QTimer(self)
                    self.timer.singleShot(1000, lambda: self.response_label_animation_reverse.start())

        elif btnName == "loginNormalButton":
            def fade_in_ln_children():
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
                self.usernameAnimation.finished.connect(
                    lambda: self.ui.username.setGraphicsEffect(self.username_shadow))
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
                self.passwordAnimation.finished.connect(
                    lambda: self.ui.password.setGraphicsEffect(self.password_shadow))
                self.passwordAnimation.start()
                self.ui.password.show()
                self.backgroundAnimation.start()

            def switchPage():
                self.ui.pages.setCurrentWidget(self.ui.password_login)
                fade_in_ln_children()

            def fade_out_ln_children():
                # Opacity fadeout for passwordLabel_3 and password_token
                self.password_label_opacity_effect = QGraphicsOpacityEffect(self.ui.passwordLabel_3)
                self.ui.passwordLabel_3.setGraphicsEffect(self.password_label_opacity_effect)
                self.password_label_opacity_effect.setOpacity(1)
                self.password_token_opacity_effect = QGraphicsOpacityEffect(self.ui.password_token)
                self.ui.password_token.setGraphicsEffect(self.password_token_opacity_effect)
                self.password_token_opacity_effect.setOpacity(1)
                self.password_label_animation = QPropertyAnimation(self.password_label_opacity_effect, b"opacity")
                self.password_label_animation.setDuration(500)
                self.password_label_animation.setStartValue(1)
                self.password_label_animation.setEndValue(0)
                self.password_label_animation.setEasingCurve(QEasingCurve.InOutQuart)
                self.password_label_animation.start()
                self.password_label_animation.finished.connect(switchPage)
                self.password_token_animation = QPropertyAnimation(self.password_token_opacity_effect, b"opacity")
                self.password_token_animation.setDuration(500)
                self.password_token_animation.setStartValue(1)
                self.password_token_animation.setEndValue(0)
                self.password_token_animation.setEasingCurve(QEasingCurve.InOutQuart)
                self.backgroundAnimationReverse.start()
                self.password_token_animation.start()
                self.password_token_animation.finished.connect(switchPage)

            fade_out_ln_children()

        elif btnName == "loginTokenButton":
            password = self.ui.password_token.text()
            if password == "":
                self.ui.responseLabel.setText("Please fill in all fields.")
                self.ui.responseLabel.setStyleSheet(
                    "background-color: #001010; color: #e51328; border-radius: 10px; font: 600 10pt \"Inter Medium\"; border: 1px solid #e51328;")
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
                        "background-color: #001010; color: rgb(99, 255, 122); border-radius: 10px; font: 600 10pt \"Inter Medium\"; border: 1px solid rgb(99, 255, 122);")
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
                        "background-color: #001010; color: #e51328; border-radius: 10px; font: 600 10pt \"Inter Medium\"; border: 1px solid #e51328;")
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
                    config["token"] = response["token"]
                    print(config)
                    with open(os.getcwd() + "/config/config.json", "w") as f:
                        json.dump(config, f)
                        f.close()
                    response, code = token_login(self.__cached_password, config["token"])
                    self.ui.twofactor_responselabel.setText("Login successful.")
                    self.ui.twofactor_responselabel.setStyleSheet(
                        "background-color: #001010; color: rgb(99, 255, 122); border-radius: 10px; font: 600 10pt \"Inter Medium\"; border: 1px solid rgb(99, 255, 122);")
                    self.stopAnimations()
                    self.twofactor_responselabel_animation.start()
                    self.timer = QTimer(self)
                    self.timer.singleShot(1000, lambda: self.successfulLogin(response))
            else:
                self.ui.twofactor_responselabel.setText(response["detail"])
                self.ui.twofactor_responselabel.setStyleSheet(
                    "background-color: #001010; color: #e51328; border-radius: 10px; font: 600 10pt \"Inter Medium\"; border: 1px solid #e51328;")
                self.stopAnimations()
                self.twofactor_responselabel_animation.start()
                self.timer = QTimer(self)
                self.timer.singleShot(1000, lambda: self.twofactor_responselabel_reverse.start())

    def openMainWindow(self, response):
        self.mainWindow = MainWindow(response, self.config)
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

        if self.ui.pages.currentWidget() == self.ui.password_login or self.ui.pages.currentWidget() == self.ui.token_login:
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
