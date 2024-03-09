from modules import *
from modules.backend_connect_to_hsm import connect_to_hsm_setup, ping_hsm, connect_to_hsm_post_setup, statistics_connector


# https://www.pythonguis.com/tutorials/multithreading-pyqt-applications-qthreadpool/
class WorkerSignals(QObject):
    '''
    Defines the signals available from a running worker thread.

    Supported signals are:

    finished
        No data

    error
        tuple (exctype, value, traceback.format_exc() )

    result
        object data returned from processing, anything

    '''
    finished = Signal()  # QtCore.Signal
    error = Signal(tuple)
    result = Signal(object)


class Worker(QRunnable):
    '''
    Worker thread

    Inherits from QRunnable to handler worker thread setup, signals and wrap-up.

    :param callback: The function callback to run on this worker thread. Supplied args and
                     kwargs will be passed through to the runner.
    :type callback: function
    :param args: Arguments to pass to the callback function
    :param kwargs: Keywords to pass to the callback function

    '''

    def __init__(self, fn, *args, **kwargs):
        super(Worker, self).__init__()
        # Store constructor arguments (re-used for processing)
        self.fn = fn
        self.args = args
        self.kwargs = kwargs
        self.signals = WorkerSignals()

    @Slot()  # QtCore.Slot
    def run(self):
        """
        Initialise the runner function with passed args, kwargs.
        """

        # Retrieve args/kwargs here; and fire processing using them
        try:
            result = self.fn(*self.args, **self.kwargs)
        except:
            trackback_str = traceback.format_exc()
            exctype, value = sys.exc_info()[:2]
            self.signals.error.emit((exctype, value, trackback_str))
        else:
            self.signals.result.emit(result)  # Return the result of the processing
        finally:
            self.signals.finished.emit()  # Done

from threading import Timer

class RepeatedTimer(object):
    def __init__(self, interval, function, *args, **kwargs):
        self._timer     = None
        self.interval   = interval
        self.function   = function
        self.args       = args
        self.kwargs     = kwargs
        self.is_running = False
        self.start()

    def _run(self):
        self.is_running = False
        self.start()
        self.function(*self.args, **self.kwargs)

    def start(self):
        if not self.is_running:
            self._timer = Timer(self.interval, self._run)
            self._timer.start()
            self.is_running = True

    def stop(self):
        self._timer.cancel()
        self.is_running = False


class MainWindow(QMainWindow):
    def __init__(self, response, config):
        QMainWindow.__init__(self)
        # SET AS GLOBAL WIDGETS
        # ///////////////////////////////////////////////////////////////
        self.stats = None
        self.statistics_hsm_connection = None
        self.timer = None
        self.__machine_identifier = None
        self.__masterpw = None
        self.dragPos = None
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.config = config
        self.threadpool = QThreadPool()

        self.cpu_view = QGraphicsView()
        self.cpu_view.setAlignment(Qt.AlignRight | Qt.AlignBottom)
        self.cpu_view.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.cpu_view.setViewportUpdateMode(QGraphicsView.SmartViewportUpdate)
        self.ui.cpu_layout.addWidget(self.cpu_view)
        self.cpu_scene = QGraphicsScene()
        self.cpu_view.setScene(self.cpu_scene)

        self.gpu_view = QGraphicsView()
        self.gpu_view.setAlignment(Qt.AlignRight | Qt.AlignBottom)
        self.gpu_view.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.gpu_view.setViewportUpdateMode(QGraphicsView.SmartViewportUpdate)
        self.ui.gpu_layout.addWidget(self.gpu_view)
        self.gpu_scene = QGraphicsScene()
        self.gpu_view.setScene(self.gpu_scene)

        self.ram_view = QGraphicsView()
        self.ram_view.setAlignment(Qt.AlignRight | Qt.AlignBottom)
        self.ram_view.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.ram_view.setViewportUpdateMode(QGraphicsView.SmartViewportUpdate)
        self.ui.ram_layout.addWidget(self.ram_view)
        self.ram_scene = QGraphicsScene()
        self.ram_view.setScene(self.ram_scene)


        # Get size of screen
        screen = QApplication.primaryScreen()
        size = screen.size()
        if isinstance(response, str):
            self.__response = json.loads(response)
        else:
            self.__response = response
        if size.width() - 20 < 1400 or size.height() - 20 < 860:
            # noinspection PyArgumentList
            self.resize(size.width() - 200, size.height() - 200)
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
        if "configuration" not in self.config or len(self.config["configuration"]) == 0:
            self.ui.pages.setCurrentWidget(self.ui.hsmlist)
            self.ui.hsmpages.setCurrentWidget(self.ui.addfirst)
        else:
            self.ui.pages.setCurrentWidget(self.ui.hsmlist)
            self.ui.overview_hsm_name.setText(self.config["configuration"][0]["name"])
            self.ui.overview_mid.setText(self.config["configuration"][0]["my_uuid"])

        def ping_hsm_result():
            self.ui.overview_auth_label.setText("Online")
            self.ui.overview_auth_label.setStyleSheet("font: 700 10pt \"Inter Medium\"; color: #12B76A;")
            self.ui.overview_auth_icon.setPixmap(QPixmap(":/icons/images/icons/authenticated.png"))
            self.ui.overview_auth_icon.setToolTip("HSM is online.")

        def ping_hsm_error():
            self.ui.overview_auth_label.setText("Offline")
            self.ui.overview_auth_label.setStyleSheet("font: 700 10pt \"Inter Medium\"; color: #F04438;")
            self.ui.overview_auth_icon.setPixmap(QPixmap(":/icons/images/icons/unauthenticated.png"))
            self.ui.overview_auth_icon.setToolTip("HSM is offline.")

        def set_masterpw():
            master_pw = self.ui.overview_masterpw_field.text()
            if master_pw == "":
                self.ui.responselabel2.setText("Please enter the master password.")
                self.response_label_2_animation.start()
                timer = QTimer()
                timer.singleShot(3000, lambda: self.response_label_2_animation_reverse.start())
                return
            else:
                self.ui.auth_area_border.setStyleSheet("border: 1px solid #12B76A; border-radius: 10px;")
                self.__masterpw = master_pw
                self.ui.overview_auth_btn.setText("MP set.")
                # Make the button not clickable
                self.ui.overview_auth_btn.setEnabled(False)
                self.ui.overview_auth_btn.setStyleSheet("background-color: #12B76A; color: white; border: 1px solid #12B76A; border-radius: 10px; border-radius: 5px; font: 600 10pt \"Inter Medium\";")
                self.ui.overview_auth_btn.setIcon(QIcon(":/icons/images/icons/authenticated.png"))
                self.ui.overview_masterpw_field.setReadOnly(True)
                self.ui.overview_icon_4.setToolTip("Master password is set. You need to restart to change this.")

        # Try to ping the HSM to determine if it is online or not.
        self.ui.auth_area_border.setStyleSheet("border: 1px solid #F04438; border-radius: 10px;")
        worker = Worker(ping_hsm, self.config["configuration"][0]["ip"])
        self.threadpool.start(worker)
        worker.signals.result.connect(ping_hsm_result)
        worker.signals.error.connect(ping_hsm_error)

        self.ui.overview_auth_btn.clicked.connect(set_masterpw)

        self.statistics_worker = Worker(statistics_connector, self.config["configuration"][0]["ip"])
        self.threadpool.start(self.statistics_worker)
        self.statistics_worker.signals.result.connect(self.statistics_handler)
        self.statistics_worker.signals.error.connect(self.statistics_error_handler)

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
        self.ui.btn_website.clicked.connect(self.buttonClick)
        self.ui.btn_addfirsthsm.clicked.connect(self.buttonClick)
        self.ui.add_button.clicked.connect(self.buttonClick)

        # ANIMATIONS
        # ///////////////////////////////////////////////////////////////

        self.hsm_name_opacity_effect = QGraphicsOpacityEffect(self.ui.hsm_name)
        self.hsm_masterpw_opacity_effect = QGraphicsOpacityEffect(self.ui.hsm_masterpw)
        self.hsm_uuid_opacity_effect = QGraphicsOpacityEffect(self.ui.hsm_uuid)
        self.hsm_ipaddress_opacity_effect = QGraphicsOpacityEffect(self.ui.hsm_ip)
        self.hsm_name_opacity_effect.setOpacity(0)
        self.hsm_masterpw_opacity_effect.setOpacity(0)
        self.hsm_uuid_opacity_effect.setOpacity(0)
        self.hsm_ipaddress_opacity_effect.setOpacity(0)
        self.hsm_name_animation = QPropertyAnimation(self.hsm_name_opacity_effect, b"opacity")
        self.hsm_masterpw_animation = QPropertyAnimation(self.hsm_masterpw_opacity_effect, b"opacity")
        self.hsm_uuid_animation = QPropertyAnimation(self.hsm_uuid_opacity_effect, b"opacity")
        self.hsm_ipaddress_animation = QPropertyAnimation(self.hsm_ipaddress_opacity_effect, b"opacity")
        self.hsm_name_animation.setDuration(500)
        self.hsm_masterpw_animation.setDuration(500)
        self.hsm_uuid_animation.setDuration(500)
        self.hsm_ipaddress_animation.setDuration(500)
        self.hsm_name_animation.setStartValue(0)
        self.hsm_masterpw_animation.setStartValue(0)
        self.hsm_uuid_animation.setStartValue(0)
        self.hsm_ipaddress_animation.setStartValue(0)
        self.hsm_name_animation.setEndValue(1)
        self.hsm_masterpw_animation.setEndValue(1)
        self.hsm_uuid_animation.setEndValue(1)
        self.hsm_ipaddress_animation.setEndValue(1)
        self.hsm_name_animation.setEasingCurve(QEasingCurve.InOutQuart)
        self.hsm_masterpw_animation.setEasingCurve(QEasingCurve.InOutQuart)
        self.hsm_uuid_animation.setEasingCurve(QEasingCurve.InOutQuart)
        self.hsm_ipaddress_animation.setEasingCurve(QEasingCurve.InOutQuart)
        self.hsm_name_animation.finished.connect(lambda: self.ui.hsm_name.setFocus())

        self.response_label_animation = QPropertyAnimation(self.ui.responselabel, b"geometry")
        self.response_label_animation.setDuration(500)
        self.response_label_animation.setStartValue(QRect(290, 471, 351, 0))
        self.response_label_animation.setEndValue(QRect(290, 400, 351, 41))
        self.response_label_animation.setEasingCurve(QEasingCurve.InBounce)

        self.response_label_animation_reverse = QPropertyAnimation(self.ui.responselabel, b"geometry")
        self.response_label_animation_reverse.setDuration(500)
        self.response_label_animation_reverse.setStartValue(QRect(290, 400, 351, 41))
        self.response_label_animation_reverse.setEndValue(QRect(290, 471, 351, 0))
        self.response_label_animation_reverse.setEasingCurve(QEasingCurve.OutBounce)
        self.response_label_animation_reverse.finished.connect(lambda: self.updateEverything)

        self.response_label_2_animation = QPropertyAnimation(self.ui.responselabel, b"geometry")
        self.response_label_2_animation.setDuration(500)
        self.response_label_2_animation.setStartValue(QRect(290, 471, 351, 0))
        self.response_label_2_animation.setEndValue(QRect(290, 400, 351, 41))
        self.response_label_2_animation.setEasingCurve(QEasingCurve.InBounce)

        self.response_label_2_animation_reverse = QPropertyAnimation(self.ui.responselabel, b"geometry")
        self.response_label_2_animation_reverse.setDuration(500)
        self.response_label_2_animation_reverse.setStartValue(QRect(290, 400, 351, 41))
        self.response_label_2_animation_reverse.setEndValue(QRect(290, 471, 351, 0))
        self.response_label_2_animation_reverse.setEasingCurve(QEasingCurve.OutBounce)
        self.response_label_2_animation_reverse.finished.connect(lambda: self.updateEverything)

        # Set on hover
        def enter_handler(_):
            # If the graphics effect is deleted, set it
            if self.ui.btn_addfirsthsm.graphicsEffect() is None:
                self.addfirstshadow = QGraphicsDropShadowEffect(self.ui.btn_addfirsthsm)
                self.addfirstshadow.setBlurRadius(25)
                self.addfirstshadow.setXOffset(0)
                self.addfirstshadow.setYOffset(0)
                self.addfirstshadow.setColor(QColor(255, 255, 255, 150))
                self.ui.btn_addfirsthsm.setGraphicsEffect(self.addfirstshadow)
            else:
                pass

        # Remove once mouse leaves
        def leave_handler(_):
            self.ui.btn_addfirsthsm.setGraphicsEffect(None)

        self.ui.btn_addfirsthsm.enterEvent = enter_handler
        self.ui.btn_addfirsthsm.leaveEvent = leave_handler

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
        except Exception as e:
            # Get the local IP address instead
            ipaddr = socket.gethostbyname(socket.gethostname())

        self.ui.ipaddress.setText(ipaddr)

        if "configuration" not in self.config or len(self.config["configuration"]) == 0:
            self.ui.hsmpages.setCurrentWidget(self.ui.addfirst)
        else:
            self.ui.hsmpages.setCurrentWidget(self.ui.overview)

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

    def updateEverything(self):
        self.repaint()
        QApplication.processEvents()

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
                webbrowser.get().open("https://docs.ameasere.com")  # SET PAGE
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
                webbrowser.get().open("https://ameasere.com/polaris/dashboard")
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
                webbrowser.get().open("https://ameasere.com/polaris/dashboard")
                self.currentPage = "settings"
                self.ui.btn_settings.setStyleSheet(base64.b64decode(self.settings_selected_stylesheet).decode("utf-8"))
                self.ui.sep4.setPixmap(QPixmap(":/icons/images/icons/separator.png"))
                self.ui.icon_4.setPixmap(QPixmap(":/icons/images/icons/settings_selected.png"))
        elif btnName == "btn_website":
            webbrowser.get().open("https://ameasere.com/polaris")
        elif btnName == "btn_addfirsthsm":
            self.ui.hsmpages.setCurrentWidget(self.ui.hsmdetails)
            self.hsm_name_animation.start()
            self.ui.hsm_name.show()
            self.ui.hsm_name.setGraphicsEffect(self.hsm_name_opacity_effect)
            self.hsm_masterpw_animation.start()
            self.ui.hsm_masterpw.show()
            self.ui.hsm_masterpw.setGraphicsEffect(self.hsm_masterpw_opacity_effect)
            self.hsm_uuid_animation.start()
            self.ui.hsm_uuid.show()
            self.ui.hsm_uuid.setGraphicsEffect(self.hsm_uuid_opacity_effect)
            self.hsm_ipaddress_animation.start()
            self.ui.hsm_ip.show()
            self.ui.hsm_ip.setGraphicsEffect(self.hsm_ipaddress_opacity_effect)
            self.ui.hsm_name.setFocus()
            self.__machine_identifier = str(uuid4())
            self.ui.hsm_uuid.setText(self.__machine_identifier[:31] + "...")
            self.hsm_name_animation.finished.connect(lambda: self.ui.hsm_name.setGraphicsEffect(None))
            self.hsm_masterpw_animation.finished.connect(lambda: self.ui.hsm_masterpw.setGraphicsEffect(None))
            self.hsm_uuid_animation.finished.connect(lambda: self.ui.hsm_uuid.setGraphicsEffect(None))
            self.hsm_ipaddress_animation.finished.connect(lambda: self.ui.hsm_ip.setGraphicsEffect(None))
            self.hsm_uuid_animation.finished.connect(lambda: self.updateWindow)
        elif btnName == "add_button":
            def is_valid(hsmip):
                try:
                    ip_obj = ipaddress.ip_address(hsmip)
                    return True
                except ValueError:
                    return False

            if any([self.ui.hsm_name.text() == "", self.ui.hsm_masterpw.text() == "", self.ui.hsm_ip.text() == ""]):
                self.ui.responselabel.setText("Please fill in all fields.")
                self.ui.responselabel.setStyleSheet(
                    "background-color: #001010; color: #e51328; border-radius: 10px; font: 600 10pt \"Inter Medium\"; border: 1px solid #e51328;")
                self.stopAnimations()
                self.response_label_animation.start()
                self.timer = QTimer(self)
                self.timer.singleShot(1500, lambda: self.response_label_animation_reverse.start())
                return
            elif not is_valid(self.ui.hsm_ip.text()):
                self.ui.hsm_ip.clear()
                self.ui.hsm_ip.setPlaceholderText("Please enter a valid IP address")
                self.ui.responselabel.setText("Please enter a valid IP address.")
                self.ui.responselabel.setStyleSheet(
                    "background-color: #001010; color: #e51328; border-radius: 10px; font: 600 10pt \"Inter Medium\"; border: 1px solid #e51328;")
                self.stopAnimations()
                self.response_label_animation.start()
                self.timer = QTimer(self)
                self.timer.singleShot(1500, lambda: self.response_label_animation_reverse.start())
                return

            def print_error(etuple):
                self.ui.responselabel.setText("An error occurred. Please try again.")
                self.ui.responselabel.setStyleSheet(
                    "background-color: #001010; color: #e51328; border-radius: 10px; font: 600 10pt \"Inter Medium\"; border: 1px solid #e51328;")
                self.stopAnimations()
                self.response_label_animation.start()
                self.timer = QTimer(self)
                self.timer.singleShot(1500, lambda: self.response_label_animation_reverse.start())

            worker = Worker(lambda: connect_to_hsm_setup(self.ui.hsm_ip.text(), self.__machine_identifier,
                                                         self.ui.hsm_masterpw.text(), self.__response["username"]))
            worker.signals.result.connect(self.setup_finished)
            worker.signals.error.connect(print_error)
            self.threadpool.start(worker)

    def updateWindow(self):
        # Process events in the event loop
        self.repaint()
        QApplication.processEvents()

    def statistics_handler(self, result):
        self.statistics_hsm_connection = result
        self.stats = RepeatedTimer(1, self.hsm_statistics)
        self.stats.start()

    def hsm_statistics(self):
        try:
            statistics = str(self.statistics_hsm_connection.recv(1024))
            statistics = statistics.replace("polaris://", "").split("/")
            cpu_statistics = statistics[0]
            cpu_percent = float(cpu_statistics.split(":")[1])
            gpu_statistics = statistics[1]
            gpu_percent = float(gpu_statistics.split(":")[1])
            ram_statistics = statistics[2]
            ram_percent = float(ram_statistics.split(":")[1])
            current_cpu = str(int(cpu_percent)) + "%"
            current_gpu = str(int(gpu_percent)) + "%"
            current_ram = str(int(ram_percent)) + "%"
            self.ui.overview_cpu_current.setText(current_cpu)
            self.ui.overview_gpu_current.setText(current_gpu)
            self.ui.overview_ram_current.setText(current_ram)
            print(f"CPU: {cpu_percent}, GPU: {gpu_percent}, RAM: {ram_percent}")
            cpu_x = len(self.cpu_scene.items()) * 5
            gpu_x = len(self.gpu_scene.items()) * 5
            ram_x = len(self.ram_scene.items()) * 5

            # Calculate the height of the bar based on CPU percentage
            cpu_bar_height = (self.cpu_view.height() - 5) * (cpu_percent / 100)
            gpu_bar_height = (self.gpu_view.height() - 5) * (gpu_percent / 100)
            ram_bar_height = (self.ram_view.height() - 5) * (ram_percent / 100)
            if cpu_bar_height < 1:
                cpu_bar_height = 1
            if gpu_bar_height < 1:
                gpu_bar_height = 1
            if ram_bar_height < 1:
                ram_bar_height = 1
            # Sort the items based on their x-coordinate
            cpu_items = sorted(self.cpu_scene.items(), key=lambda x: x.rect().x())
            gpu_items = sorted(self.gpu_scene.items(), key=lambda x: x.rect().x())
            ram_items = sorted(self.ram_scene.items(), key=lambda x: x.rect().x())

            # Remove the first item if the total width of all bars exceeds the view width
            while len(cpu_items) * 5 > self.cpu_view.width() - 30:
                item = cpu_items.pop(0)
                self.cpu_scene.removeItem(item)
                for item in cpu_items:
                    item.setRect(QRectF(item.rect().x() - 5, item.rect().y(), item.rect().width(), item.rect().height()))
                cpu_x = (len(cpu_items) * 5) - 5

            while len(gpu_items) * 5 > self.gpu_view.width() - 30:
                item = gpu_items.pop(0)
                self.gpu_scene.removeItem(item)
                for item in gpu_items:
                    item.setRect(QRectF(item.rect().x() - 5, item.rect().y(), item.rect().width(), item.rect().height()))
                gpu_x = (len(gpu_items) * 5) - 5

            while len(ram_items) * 5 > self.ram_view.width() - 30:
                item = ram_items.pop(0)
                self.ram_scene.removeItem(item)
                for item in ram_items:
                    item.setRect(QRectF(item.rect().x() - 5, item.rect().y(), item.rect().width(), item.rect().height()))
                ram_x = (len(ram_items) * 5) - 5

            # Draw a bar representing CPU usage
            try:
                cpu_bar = QGraphicsRectItem(cpu_x, self.cpu_view.height() - cpu_bar_height, 5, cpu_bar_height)
                # Set brush with 9e77ed
                cpu_bar.setBrush(QColor("#9e77ed"))
                self.cpu_scene.addItem(cpu_bar)
                self.cpu_scene.update(self.cpu_scene.sceneRect())
                print(f"Bar added at x: {cpu_x}, height: {cpu_bar_height}")

                gpu_bar = QGraphicsRectItem(gpu_x, self.gpu_view.height() - gpu_bar_height, 5, gpu_bar_height)
                gpu_bar.setBrush(QColor("#9e77ed"))
                self.gpu_scene.addItem(gpu_bar)
                self.gpu_scene.update(self.gpu_scene.sceneRect())
                print(f"Bar added at x: {gpu_x}, height: {gpu_bar_height}")

                ram_bar = QGraphicsRectItem(ram_x, self.ram_view.height() - ram_bar_height, 5, ram_bar_height)
                ram_bar.setBrush(QColor("#9e77ed"))
                self.ram_scene.addItem(ram_bar)
                self.ram_scene.update(self.ram_scene.sceneRect())
                print(f"Bar added at x: {ram_x}, height: {ram_bar_height}")

            except Exception as e:
                print(e)
        except TimeoutError:
            print("Timeout error occurred.")

    def statistics_error_handler(self, etuple):
        self.statistics_hsm_connection = None
        print(etuple)

    def setup_finished(self, response):
        def overview_transition():
            self.ui.hsmpages.setCurrentWidget(self.ui.overview)

        if response == "polaris://mid:success":
            self.ui.responselabel.setText("HSM setup successful.")
            self.ui.responselabel.setStyleSheet(
                "background-color: #001010; color: #00ff00; border-radius: 10px; font: 600 10pt \"Inter Medium\"; border: 1px solid #00ff00;")
            self.stopAnimations()
            self.response_label_animation.start()
            if "configuration" not in self.config:
                self.config["configuration"] = []
            self.config["configuration"].append(
                {"name": self.ui.hsm_name.text(), "ip": self.ui.hsm_ip.text(), "my_uuid": self.__machine_identifier})
            print(self.config)
            with open(os.getcwd() + "/config/config.json", "w") as f:
                f.write(json.dumps(self.config))
                f.close()
            self.ui.hsm_name.clear()
            self.ui.hsm_masterpw.clear()
            self.ui.hsm_ip.clear()
            self.ui.hsm_name.setText("Name")
            self.ui.hsm_masterpw.setText("Master Password")
            self.ui.hsm_ip.setText("IP Address")
            self.ui.hsm_uuid.setText("UUID")
            self.timer = QTimer(self)
            self.timer.singleShot(1500, lambda: self.response_label_animation_reverse.start())
            self.timer.singleShot(1500, lambda: overview_transition)
            # Add HSM to the overview page.
            # TODO
        else:
            self.ui.responselabel.setText("HSM setup failed.")
            self.ui.responselabel.setStyleSheet(
                "background-color: #001010; color: #e51328; border-radius: 10px; font: 600 10pt \"Inter Medium\"; border: 1px solid #e51328;")
            self.stopAnimations()
            self.response_label_animation.start()
            self.timer = QTimer(self)
            self.timer.singleShot(1500, lambda: self.response_label_animation_reverse.start())

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

    def fadeout(self):
        # Fade out animation
        self.fadeOutAnimation = QPropertyAnimation(self, b"windowOpacity")
        self.fadeOutAnimation.setDuration(350)
        self.fadeOutAnimation.setStartValue(1)
        self.fadeOutAnimation.setEndValue(0)
        self.fadeOutAnimation.setEasingCurve(QEasingCurve.InOutQuart)
        # Start after a QTimer of 1 second
        self.timer = QTimer(self)
        self.timer.singleShot(200, lambda: self.fadeOutAnimation.start())
        self.fadeOutAnimation.finished.connect(lambda: self.close())

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
            self.ui.btn_website.show()

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
        self.profilepicAnimation.setEndValue(0.99)
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
