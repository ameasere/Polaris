from modules import *
from modules.backend_connect_to_hsm import connect_to_hsm_setup, ping_hsm, connect_to_hsm_post_setup, \
    statistics_connector


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


class HSMConnector(QObject):
    finished = Signal(str)
    exception_signal = Signal(str)

    def __init__(self, ip, machine_identifier, master_password, username, action_string):
        super().__init__()
        self.ip = ip
        self.machine_identifier = machine_identifier
        self.master_password = master_password
        self.username = username
        self.action_string = action_string

    def run(self):
        try:
            response = connect_to_hsm_post_setup(self.ip, self.machine_identifier, self.master_password, self.username, self.action_string)
            self.finished.emit(response)
        except Exception as e:
            print(repr(e))
            self.exception_signal.emit(str(e))


class NetworkWorker(QObject):
    finished = Signal()
    progress_signal = Signal(str)
    exception_signal = Signal(str)

    def __init__(self, ip):
        super().__init__()
        self.ip = ip
        self.connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.connection.connect((self.ip, 26556))
            self.connected = True
        except Exception as e:
            print(e)
            self.connected = False
            self.exception_signal.emit(str(e))

    def connect_to_server(self):
        try:
            self.connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.connection.connect((self.ip, 26556))
            self.connected = True
        except Exception as e:
            self.exception_signal.emit(str(e))
            time.sleep(1)

    def run(self):
        while True:
            if not self.connected:
                self.connect_to_server()

            try:
                statistics = self.connection.recv(1024).decode("utf-8")
                if not statistics:
                    self.connected = False
                    self.connection.close()
                    self.exception_signal.emit("Connection lost. Reconnecting...")
                    time.sleep(1)
                    continue
                self.progress_signal.emit(statistics)
                time.sleep(1)
            except Exception as e:
                self.connected = False
                self.connection.close()
                self.exception_signal.emit(str(e))
                time.sleep(1)
                continue

        self.finished.emit()


class MainWindow(QMainWindow):
    def __init__(self, response, config):
        QMainWindow.__init__(self)
        # SET AS GLOBAL WIDGETS
        # ///////////////////////////////////////////////////////////////
        self.stats = None
        self.timer = None
        self.__machine_identifier = None
        self.__masterpw = None
        self.dragPos = None
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.config = config
        self.threadpool = QThreadPool()
        self.time_since_update = 0
        self.ui.last_update_label.setText("Never")

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

        self.btn_controlpanel_disabled = "I2J0bl9jb250cm9scGFuZWwgewpiYWNrZ3JvdW5kLWNvbG9yOiB0cmFuc3BhcmVudDsKZm9udDogNjAwIDEwcHQgIkludGVyIE1lZGl1bSI7CnRleHQtYWxpZ246IGNlbnRlcjsKY29sb3I6ICNmZmY7CmJvcmRlcjogc29saWQ7CmJvcmRlci1ib3R0b206IDJweCBzb2xpZCByZ2IoMTc2LCAxNzYsIDE3Nik7Cn0KI2J0bl9jb250cm9scGFuZWw6aG92ZXIgewpiYWNrZ3JvdW5kLWNvbG9yOiB0cmFuc3BhcmVudDsKZm9udDogNjAwIDEwcHQgIkludGVyIE1lZGl1bSI7CnRleHQtYWxpZ246IGNlbnRlcjsKY29sb3I6ICNmZmY7CmJvcmRlcjogc29saWQ7CmJvcmRlci1ib3R0b206IDJweCBzb2xpZCByZ2IoMTc2LCAxNzYsIDE3Nik7Cn0KI2J0bl9jb250cm9scGFuZWw6cHJlc3NlZCB7CmJhY2tncm91bmQtY29sb3I6IHRyYW5zcGFyZW50Owpmb250OiA2MDAgMTBwdCAiSW50ZXIgTWVkaXVtIjsKdGV4dC1hbGlnbjogY2VudGVyOwpjb2xvcjogIzllNzdlZDsKYm9yZGVyOiBzb2xpZDsKYm9yZGVyLWJvdHRvbTogMnB4IHNvbGlkIHJnYigxNzYsIDE3NiwgMTc2KTsKfQ=="
        self.btn_configurator_disabled = "I2J0bl9jb25maWd1cmF0b3J7CmJhY2tncm91bmQtY29sb3I6IHRyYW5zcGFyZW50Owpmb250OiA2MDAgMTBwdCAiSW50ZXIgTWVkaXVtIjsKdGV4dC1hbGlnbjogY2VudGVyOwpjb2xvcjogI2ZmZjsKYm9yZGVyOiBzb2xpZDsKYm9yZGVyLWJvdHRvbTogMnB4IHNvbGlkIHJnYigxNzYsIDE3NiwgMTc2KTsKfQojYnRuX2NvbmZpZ3VyYXRvcjpob3ZlciB7CmJhY2tncm91bmQtY29sb3I6IHRyYW5zcGFyZW50Owpmb250OiA2MDAgMTBwdCAiSW50ZXIgTWVkaXVtIjsKdGV4dC1hbGlnbjogY2VudGVyOwpjb2xvcjogI2ZmZjsKYm9yZGVyOiBzb2xpZDsKYm9yZGVyLWJvdHRvbTogMnB4IHNvbGlkIHJnYigxNzYsIDE3NiwgMTc2KTsKfQojYnRuX2NvbmZpZ3VyYXRvcjpwcmVzc2VkIHsKYmFja2dyb3VuZC1jb2xvcjogdHJhbnNwYXJlbnQ7CmZvbnQ6IDYwMCAxMHB0ICJJbnRlciBNZWRpdW0iOwp0ZXh0LWFsaWduOiBjZW50ZXI7CmNvbG9yOiAjOWU3N2VkOwpib3JkZXI6IHNvbGlkOwpib3JkZXItYm90dG9tOiAycHggc29saWQgcmdiKDE3NiwgMTc2LCAxNzYpOwp9"
        self.btn_controlpanel_enabled = "I2J0bl9jb250cm9scGFuZWwgewpiYWNrZ3JvdW5kLWNvbG9yOiB0cmFuc3BhcmVudDsKZm9udDogNjAwIDEwcHQgIkludGVyIE1lZGl1bSI7CnRleHQtYWxpZ246IGNlbnRlcjsKY29sb3I6ICNmZmY7CmJvcmRlcjogc29saWQ7CmJvcmRlci1ib3R0b206IDJweCBzb2xpZCAjOWU3N2VkOwp9CiNidG5fY29udHJvbHBhbmVsOmhvdmVyIHsKYmFja2dyb3VuZC1jb2xvcjogdHJhbnNwYXJlbnQ7CmZvbnQ6IDYwMCAxMHB0ICJJbnRlciBNZWRpdW0iOwp0ZXh0LWFsaWduOiBjZW50ZXI7CmNvbG9yOiAjZmZmOwpib3JkZXI6IHNvbGlkOwpib3JkZXItYm90dG9tOiAycHggc29saWQgIzllNzdlZDsKfQojYnRuX2NvbnRyb2xwYW5lbDpwcmVzc2VkIHsKYmFja2dyb3VuZC1jb2xvcjogdHJhbnNwYXJlbnQ7CmZvbnQ6IDYwMCAxMHB0ICJJbnRlciBNZWRpdW0iOwp0ZXh0LWFsaWduOiBjZW50ZXI7CmNvbG9yOiAjOWU3N2VkOwpib3JkZXI6IHNvbGlkOwpib3JkZXItYm90dG9tOiAycHggc29saWQgIzllNzdlZDsKfQ=="
        self.btn_configurator_enabled = "I2J0bl9jb25maWd1cmF0b3IgewpiYWNrZ3JvdW5kLWNvbG9yOiB0cmFuc3BhcmVudDsKZm9udDogNjAwIDEwcHQgIkludGVyIE1lZGl1bSI7CnRleHQtYWxpZ246IGNlbnRlcjsKY29sb3I6ICNmZmY7CmJvcmRlcjogc29saWQ7CmJvcmRlci1ib3R0b206IDJweCBzb2xpZCAjOWU3N2VkOwp9CiNidG5fY29uZmlndXJhdG9yOmhvdmVyIHsKYmFja2dyb3VuZC1jb2xvcjogdHJhbnNwYXJlbnQ7CmZvbnQ6IDYwMCAxMHB0ICJJbnRlciBNZWRpdW0iOwp0ZXh0LWFsaWduOiBjZW50ZXI7CmNvbG9yOiAjZmZmOwpib3JkZXI6IHNvbGlkOwpib3JkZXItYm90dG9tOiAycHggc29saWQgIzllNzdlZDsKfQojYnRuX2NvbmZpZ3VyYXRvcjpwcmVzc2VkIHsKYmFja2dyb3VuZC1jb2xvcjogdHJhbnNwYXJlbnQ7CmZvbnQ6IDYwMCAxMHB0ICJJbnRlciBNZWRpdW0iOwp0ZXh0LWFsaWduOiBjZW50ZXI7CmNvbG9yOiAjOWU3N2VkOwpib3JkZXI6IHNvbGlkOwpib3JkZXItYm90dG9tOiAycHggc29saWQgIzllNzdlZDsKfQ=="
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

            self.ui.configurator_bg.setStyleSheet("background-color: qlineargradient(spread:pad, x1:0.511364, y1:0, x2:0.5, y2:1, stop:0 rgba(0, 0, 0, 255), stop:1 rgba(132, 132, 132, 255))")
            self.ui.controlpanel_bg.setStyleSheet("background-color: qlineargradient(spread:pad, x1:0.511364, y1:0, x2:0.5, y2:1, stop:0 rgba(0, 0, 0, 255), stop:1 rgba(132, 132, 132, 255))")
            self.ui.btn_controlpanel.setStyleSheet(base64.b64decode(self.btn_controlpanel_disabled).decode("utf-8"))
            self.ui.btn_configurator.setStyleSheet(base64.b64decode(self.btn_configurator_disabled).decode("utf-8"))
            self.ui.btn_controlpanel.setEnabled(False)
            self.ui.btn_configurator.setEnabled(False)
        else:
            self.ui.pages.setCurrentWidget(self.ui.hsmlist)
            self.ui.overview_hsm_name.setText(self.config["configuration"][0]["name"])
            self.ui.overview_mid.setText(self.config["configuration"][0]["my_uuid"])
            self.networker = NetworkWorker(self.config["configuration"][0]["ip"])
            self.statsthread = QThread()
            self.networker.moveToThread(self.statsthread)
            self.statsthread.started.connect(self.networker.run)
            self.networker.progress_signal.connect(self.hsm_statistics)
            self.networker.exception_signal.connect(self.hsm_statistics_error)
            self.statsthread.start()

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
                self.ui.overview_responselabel.setText("Please enter the master password.")
                self.ui.overview_responselabel.setStyleSheet(
                    "background-color: #001010; color: #e51328; border-radius: 10px; font: 600 10pt \"Inter Medium\"; border: 1px solid #e51328;")
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
                self.ui.overview_auth_btn.setStyleSheet(
                    "background-color: #12B76A; color: white; border: 1px solid #12B76A; border-radius: 10px; border-radius: 5px; font: 600 10pt \"Inter Medium\";")
                self.ui.overview_auth_btn.setIcon(QIcon(":/icons/images/icons/authenticated.png"))
                self.ui.overview_masterpw_field.setReadOnly(True)
                self.ui.overview_icon_4.setToolTip("Master password is set. You need to restart to change this.")
                self.ui.overview_responselabel.setText("Master password set.")
                self.ui.overview_responselabel.setStyleSheet(
                    "background-color: #001010; color: #12B76A; border-radius: 10px; font: 600 10pt \"Inter Medium\"; border: 1px solid #12B76A;")
                self.response_label_2_animation.start()
                timer = QTimer()
                timer.singleShot(3000, lambda: self.response_label_2_animation_reverse.start())

        # Try to ping the HSM to determine if it is online or not.
        self.ui.auth_area_border.setStyleSheet("border: 1px solid #F04438; border-radius: 10px;")
        if "configuration" not in self.config or len(self.config["configuration"]) == 0:
            ping_hsm_error()
        else:
            worker = Worker(ping_hsm, self.config["configuration"][0]["ip"])
            self.threadpool.start(worker)
            worker.signals.result.connect(ping_hsm_result)
            worker.signals.error.connect(ping_hsm_error)

        self.ui.overview_auth_btn.clicked.connect(set_masterpw)
        self.ui.btn_hsmlist.clicked.connect(self.buttonClick)
        self.ui.btn_sendcommand.clicked.connect(self.buttonClick)

        self.ui.algorithm_dd.addItems([algorithm for algorithm in hashlib.algorithms_available])
        # Sort items into alphabetical order
        self.ui.algorithm_dd.model().sort(0)

        def category_dd_changed():
            if self.ui.category_dd.currentText() == "Hashing":
                self.ui.algorithm_dd.clear()
                self.ui.algorithm_dd.addItems([algorithm for algorithm in hashlib.algorithms_available])
                # Sort items into alphabetical order
                self.ui.algorithm_dd.model().sort(0)
            elif self.ui.category_dd.currentText() == "Encryption":
                self.ui.algorithm_dd.clear()
                self.ui.algorithm_dd.addItems(["AES", "RSA", "DES", "3DES", "Blowfish", "Twofish"])
            elif self.ui.category_dd.currentText() == "Generators":
                self.ui.algorithm_dd.clear()
                self.ui.algorithm_dd.addItems(["UUID4", "Random", "RandomString", "RandomNumber"])

        self.ui.category_dd.currentIndexChanged.connect(category_dd_changed)
        self.ui.category_dd.setCurrentIndex(0)

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

        self.response_label_2_animation = QPropertyAnimation(self.ui.overview_responselabel, b"geometry")
        self.response_label_2_animation.setDuration(500)
        self.response_label_2_animation.setStartValue(QRect(0, 471, 351, 0))
        self.response_label_2_animation.setEndValue(QRect(0, 400, 351, 41))
        self.response_label_2_animation.setEasingCurve(QEasingCurve.InBounce)

        self.response_label_2_animation_reverse = QPropertyAnimation(self.ui.overview_responselabel, b"geometry")
        self.response_label_2_animation_reverse.setDuration(500)
        self.response_label_2_animation_reverse.setStartValue(QRect(0, 400, 351, 41))
        self.response_label_2_animation_reverse.setEndValue(QRect(0, 471, 351, 0))
        self.response_label_2_animation_reverse.setEasingCurve(QEasingCurve.OutBounce)
        self.response_label_2_animation_reverse.finished.connect(lambda: self.updateEverything)

        # Shadow to make auth_area_border feel 3D
        self.auth_area_border_shadow = QGraphicsDropShadowEffect(self.ui.auth_area_border)
        self.auth_area_border_shadow.setBlurRadius(25)
        self.auth_area_border_shadow.setXOffset(0)
        self.auth_area_border_shadow.setYOffset(0)
        self.auth_area_border_shadow.setColor(QColor(255, 255, 255, 150))
        self.ui.auth_area_border.setGraphicsEffect(self.auth_area_border_shadow)

        self.cpu_area_border_shadow = QGraphicsDropShadowEffect(self.ui.cpu_area_border)
        self.cpu_area_border_shadow.setBlurRadius(25)
        self.cpu_area_border_shadow.setXOffset(0)
        self.cpu_area_border_shadow.setYOffset(0)
        self.cpu_area_border_shadow.setColor(QColor(255, 255, 255, 150))
        self.ui.cpu_area_border.setGraphicsEffect(self.cpu_area_border_shadow)

        self.gpu_area_border_shadow = QGraphicsDropShadowEffect(self.ui.gpu_area_border)
        self.gpu_area_border_shadow.setBlurRadius(25)
        self.gpu_area_border_shadow.setXOffset(0)
        self.gpu_area_border_shadow.setYOffset(0)
        self.gpu_area_border_shadow.setColor(QColor(255, 255, 255, 150))
        self.ui.gpu_area_border.setGraphicsEffect(self.gpu_area_border_shadow)

        self.ram_area_border_shadow = QGraphicsDropShadowEffect(self.ui.ram_area_border)
        self.ram_area_border_shadow.setBlurRadius(25)
        self.ram_area_border_shadow.setXOffset(0)
        self.ram_area_border_shadow.setYOffset(0)
        self.ram_area_border_shadow.setColor(QColor(255, 255, 255, 150))
        self.ui.ram_area_border.setGraphicsEffect(self.ram_area_border_shadow)

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
            elif self.ui.btn_earlybird.graphicsEffect() is None:
                self.earlybirdshadow = QGraphicsDropShadowEffect(self.ui.btn_earlybird)
                self.earlybirdshadow.setBlurRadius(25)
                self.earlybirdshadow.setXOffset(0)
                self.earlybirdshadow.setYOffset(0)
                self.earlybirdshadow.setColor(QColor(255, 255, 255, 150))
                self.ui.btn_earlybird.setGraphicsEffect(self.earlybirdshadow)
            else:
                pass

        # Remove once mouse leaves
        def leave_handler(_):
            self.ui.btn_addfirsthsm.setGraphicsEffect(None)
            self.ui.btn_earlybird.setGraphicsEffect(None)

        self.ui.btn_addfirsthsm.enterEvent = enter_handler
        self.ui.btn_addfirsthsm.leaveEvent = leave_handler

        # widgets.settingsTopBtn.hide()

        self.ui.btn_earlybird.clicked.connect(self.buttonClick)
        self.ui.btn_configurator.clicked.connect(self.buttonClick)
        self.ui.btn_controlpanel.clicked.connect(self.buttonClick)

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
            self.ui.hsmpages.setCurrentWidget(self.ui.addfirst) # Setup page
        else:
            self.ui.hsmpages.setCurrentWidget(self.ui.overview) # Dashboard page

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
            if hasattr(self, "statsthread"):
                self.statsthread.quit()
                self.statsthread.wait(deadline=1000)
            self.close()
            sys.exit(0)

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
        elif btnName == "btn_earlybird":
            self.ui.pages.setCurrentWidget(self.ui.hsmlist)
            self.ui.hsmpages.setCurrentWidget(self.ui.overview)
        elif btnName == "btn_controlpanel":
            self.ui.pages.setCurrentWidget(self.ui.controlpanel)
        elif btnName == "btn_configurator":
            self.ui.pages.setCurrentWidget(self.ui.configurator)
        elif btnName == "btn_hsmlist":
            self.ui.pages.setCurrentWidget(self.ui.hsmlist)
            self.ui.hsmpages.setCurrentWidget(self.ui.overview)
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

        elif btnName == "btn_sendcommand":
            if self.ui.send_pte.toPlainText() == "" and (self.ui.algorithm_dd.currentText() != "RSA" and self.ui.category_dd.currentText() != "Generators"):
                self.ui.response_pte.setPlainText("Please enter an input!")
                return
            elif self.__masterpw == "" or self.__masterpw is None:
                self.ui.response_pte.setPlainText("Please set the master password!")
                return
            else:
                self.ui.response_pte.setPlainText("Processing...")
                self.ui.response_pte.setStyleSheet("color: #12B76A; font: 600 10pt \"Inter Medium\";background-color: rgb(33, 37, 43);")
                self.ui.response_pte.repaint()
                QApplication.processEvents()
                action = self.ui.algorithm_dd.currentText().lower()
                category = self.ui.category_dd.currentText().lower()
                if action != "rsa" or category != "generators":
                    user_in = self.ui.send_pte.toPlainText()
                    action_string = f"polaris://{action}:{user_in}"
                else:
                    action_string = f"polaris://{action}"
                self.connectthread = QThread()
                self.connector = HSMConnector(self.config["configuration"][0]["ip"], self.config["configuration"][0]["my_uuid"], self.__masterpw, self.config["username"], action_string)
                self.connector.moveToThread(self.connectthread)
                self.connectthread.started.connect(self.connector.run)
                self.connector.finished.connect(self.hsmconnector_progress)
                self.connector.exception_signal.connect(self.hsmconnector_progress)
                self.ui.btn_sendcommand.setEnabled(False)
                self.ui.btn_sendcommand.setStyleSheet("QPushButton {background-color: #b0b0b0;font: 600 10pt \"Inter Medium\";border-radius: 5px;}QPushButton:hover {background-color: #b0b0b0;border-radius: 4px;}QPushButton:pressed {	background-color: #b0b0b0;font: 600 10pt \"Inter Medium\";icon: url(:/icons/images/icons/log-in_purple.png);border-radius: 5px;}")
                self.connectthread.start()

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
                if etuple[1] == "polaris://mid:failure":
                    self.ui.responselabel.setText("Please restart the application and try again.")
                else:
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

    def hsmconnector_progress(self, response):
        response = response.replace("polaris://", "")
        # Replace the action at the start and the : afterwards.
        action = response.split(":")[0]
        response = response.replace(response.split(":")[0] + ":", "")
        if action == "rsa":
            # Split the data: the data is formatted as [pub]<base64>:[priv]<base64>
            response = response.split(":")
            pub = response[0].replace("[pub]", "")
            priv = response[1].replace("[priv]", "")
            self.ui.response_pte.setPlainText(f"Public Key: {pub}\n\nPrivate Key: {priv}")
        else:
            self.ui.response_pte.setPlainText(response)
        if "error" in response or "failure" in response:
            self.ui.response_pte.setStyleSheet("color: #e51328; font: 600 10pt \"Inter Medium\";background-color: rgb(33, 37, 43);")
        self.ui.response_pte.setStyleSheet("color: #12B76A; font: 600 10pt \"Inter Medium\";background-color: rgb(33, 37, 43);")
        self.ui.btn_sendcommand.setEnabled(True)
        self.ui.btn_sendcommand.setStyleSheet("QPushButton {background-color: #9e77ed;font: 600 10pt \"Inter Medium\";border-radius: 5px;}QPushButton:hover {background-color: rgb(168, 128, 255);border-radius: 4px;}QPushButton:pressed {	background-color: rgb(255, 243, 239);font: 600 10pt \"Inter Medium\";icon: url(:/icons/images/icons/log-in_purple.png);color: #9e77ed;border-radius: 5px;}")
        self.ui.response_pte.repaint()
        QApplication.processEvents()
        self.connectthread.quit()

    def updateWindow(self):
        # Process events in the event loop
        self.repaint()
        QApplication.processEvents()

    def hsm_statistics(self, statistics):
        try:
            if statistics == "b''":
                self.hsm_statistics_error("No statistics received.")
                self.ui.configurator_bg.setStyleSheet(
                    "background-color: qlineargradient(spread:pad, x1:0.511364, y1:0, x2:0.5, y2:1, stop:0 rgba(0, 0, 0, 255), stop:1 rgba(132, 132, 132, 255))")
                self.ui.controlpanel_bg.setStyleSheet(
                    "background-color: qlineargradient(spread:pad, x1:0.511364, y1:0, x2:0.5, y2:1, stop:0 rgba(0, 0, 0, 255), stop:1 rgba(132, 132, 132, 255))")
                self.ui.btn_controlpanel.setStyleSheet(base64.b64decode(self.btn_controlpanel_disabled).decode("utf-8"))
                self.ui.btn_configurator.setStyleSheet(base64.b64decode(self.btn_configurator_disabled).decode("utf-8"))
                self.ui.btn_controlpanel.setEnabled(False)
                self.ui.btn_configurator.setEnabled(False)
                self.ui.pages.setCurrentWidget(self.ui.hsmlist)
                self.ui.hsmpages.setCurrentWidget(self.ui.overview)
                return
            else:
                if self.ui.overview_auth_label.text() == "Offline":
                    self.ui.overview_auth_label.setText("Online")
                    self.ui.overview_auth_label.setStyleSheet("font: 700 10pt \"Inter Medium\"; color: #12B76A;")
                    self.ui.overview_auth_icon.setPixmap(QPixmap(":/icons/images/icons/authenticated.png"))
                    self.ui.overview_auth_icon.setToolTip("HSM is online.")
                    self.ui.controlpanel_bg.setStyleSheet("background-color: qlineargradient(spread:pad, x1:0.494, y1:0, x2:0.494, y2:1, stop:0 rgba(0, 9, 31, 100), stop:1 rgba(157, 122, 222, 80));")
                    self.ui.configurator_bg.setStyleSheet("background-color: qlineargradient(spread:pad, x1:0.494, y1:0, x2:0.494, y2:1, stop:0 rgba(0, 9, 31, 100), stop:1 rgba(157, 122, 222, 80));")
                    self.ui.btn_controlpanel.setEnabled(True)
                    self.ui.btn_configurator.setEnabled(True)
                    self.ui.btn_controlpanel.setStyleSheet(base64.b64decode(self.btn_controlpanel_enabled).decode("utf-8"))
                    self.ui.btn_configurator.setStyleSheet(base64.b64decode(self.btn_configurator_enabled).decode("utf-8"))
            self.time_since_update = 0
            # Get time now in DD/MM/YYYY HH:MM:SS format
            now = datetime.now()
            current_time = now.strftime("%d/%m/%Y %H:%M:%S")
            self.last_updated = now
            self.update_time = f"{self.time_since_update} seconds ago ({current_time})"
            self.ui.last_update_label.setText(self.update_time)
            statistics_array = statistics.replace("polaris://", "").split("/")
            cpu_statistics = statistics_array[0]
            cpu_percent = float(cpu_statistics.split(":")[1])
            gpu_statistics = statistics_array[1]
            gpu_percent = float(gpu_statistics.split(":")[1])
            ram_statistics = statistics_array[2]
            ram_percent = float(ram_statistics.split(":")[1])
            disk_statistics = statistics_array[3].replace("'", "")
            disk_percent = float(disk_statistics.split(":")[1])
            current_cpu = str(int(cpu_percent)) + "%"
            current_gpu = str(int(gpu_percent)) + "%"
            current_ram = str(int(ram_percent)) + "%"
            current_disk = str(int(disk_percent)) + "%"
            self.ui.overview_cpu_current.setText(current_cpu)
            self.ui.overview_gpu_current.setText(current_gpu)
            self.ui.overview_ram_current.setText(current_ram)
            self.ui.overview_disk_current.setText(current_disk)
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
            if len(cpu_items) * 5 > self.cpu_view.width() - 20:
                item = cpu_items.pop(0)
                self.cpu_scene.removeItem(item)
                for item in cpu_items:
                    item.setRect(
                        QRectF(item.rect().x() - 5, item.rect().y(), item.rect().width(), item.rect().height()))
                cpu_x = (len(cpu_items) * 5) - 5

            if len(gpu_items) * 5 > self.gpu_view.width() - 20:
                item = gpu_items.pop(0)
                self.gpu_scene.removeItem(item)
                for item in gpu_items:
                    item.setRect(
                        QRectF(item.rect().x() - 5, item.rect().y(), item.rect().width(), item.rect().height()))
                gpu_x = (len(gpu_items) * 5) - 5

            if len(ram_items) * 5 > self.ram_view.width() - 20:
                item = ram_items.pop(0)
                self.ram_scene.removeItem(item)
                for item in ram_items:
                    item.setRect(
                        QRectF(item.rect().x() - 5, item.rect().y(), item.rect().width(), item.rect().height()))
                ram_x = (len(ram_items) * 5) - 5

            # Draw a bar representing CPU usage
            try:
                cpu_bar = QGraphicsRectItem(cpu_x, self.cpu_view.height() - cpu_bar_height, 5, cpu_bar_height)
                # Set brush with 9e77ed
                cpu_bar.setBrush(QColor("#9e77ed"))
                self.cpu_scene.addItem(cpu_bar)
                self.cpu_scene.update(self.cpu_scene.sceneRect())

                gpu_bar = QGraphicsRectItem(gpu_x, self.gpu_view.height() - gpu_bar_height, 5, gpu_bar_height)
                gpu_bar.setBrush(QColor("#9e77ed"))
                self.gpu_scene.addItem(gpu_bar)
                self.gpu_scene.update(self.gpu_scene.sceneRect())

                ram_bar = QGraphicsRectItem(ram_x, self.ram_view.height() - ram_bar_height, 5, ram_bar_height)
                ram_bar.setBrush(QColor("#9e77ed"))
                self.ram_scene.addItem(ram_bar)
                self.ram_scene.update(self.ram_scene.sceneRect())

                self.ui.disk_progress_bar.setValue(int(disk_percent))

            except Exception as e:
                print(e)
        except TimeoutError:
            print("Timeout error occurred.")

    def hsm_statistics_error(self, error):
        self.ui.overview_auth_label.setText("Offline")
        self.ui.overview_auth_label.setStyleSheet("font: 700 10pt \"Inter Medium\"; color: #e51328;")
        self.ui.overview_auth_icon.setPixmap(QPixmap(":/icons/images/icons/unauthenticated.png"))
        self.ui.overview_auth_icon.setToolTip("HSM is offline.")
        self.time_since_update += 1
        self.ui.configurator_bg.setStyleSheet(
            "background-color: qlineargradient(spread:pad, x1:0.511364, y1:0, x2:0.5, y2:1, stop:0 rgba(0, 0, 0, 255), stop:1 rgba(132, 132, 132, 255))")
        self.ui.controlpanel_bg.setStyleSheet(
            "background-color: qlineargradient(spread:pad, x1:0.511364, y1:0, x2:0.5, y2:1, stop:0 rgba(0, 0, 0, 255), stop:1 rgba(132, 132, 132, 255))")
        self.ui.btn_controlpanel.setStyleSheet(base64.b64decode(self.btn_controlpanel_disabled).decode("utf-8"))
        self.ui.btn_configurator.setStyleSheet(base64.b64decode(self.btn_configurator_disabled).decode("utf-8"))
        self.ui.btn_controlpanel.setEnabled(False)
        self.ui.btn_configurator.setEnabled(False)
        self.ui.pages.setCurrentWidget(self.ui.hsmlist)
        self.ui.hsmpages.setCurrentWidget(self.ui.overview)
        if hasattr(self, "last_updated"):
            now = datetime.now()
            # Seconds between now and self.last_updated will be the self.time_since_update
            self.time_since_update = (now - self.last_updated).seconds
            self.update_time = f"{self.time_since_update} seconds ago ({self.last_updated.strftime('%d/%m/%Y %H:%M:%S')})"
        else:
            self.update_time = f"Never"
        self.ui.last_update_label.setText(self.update_time)
        print(f"Error occurred: {error}")

    def setup_finished(self, response):
        def overview_transition():
            print("Transitioning to overview page.")
            self.ui.hsmpages.setCurrentWidget(self.ui.overview)
            self.ui.overview_hsm_name.setText(self.config["configuration"][0]["name"])
            self.ui.overview_mid.setText(self.__machine_identifier)
            self.networker = NetworkWorker(self.config["configuration"][0]["ip"])
            self.statsthread = QThread()
            self.networker.moveToThread(self.statsthread)
            self.statsthread.started.connect(self.networker.run)
            self.networker.progress_signal.connect(self.hsm_statistics)
            self.networker.exception_signal.connect(self.hsm_statistics_error)
            self.statsthread.start()

        if response == "polaris://mid:success":
            self.ui.responselabel.setText("HSM setup successful.")
            self.ui.responselabel.setStyleSheet(
                "background-color: #001010; color: #12B76A; border-radius: 10px; font: 600 10pt \"Inter Medium\"; border: 1px solid #12B76A;")
            self.stopAnimations()
            self.response_label_animation.start()
            if "configuration" not in self.config:
                self.config["configuration"] = []
            self.config["configuration"].append(
                {"name": self.ui.hsm_name.text(), "ip": self.ui.hsm_ip.text(), "my_uuid": self.__machine_identifier})
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
            self.timer.singleShot(2000, overview_transition)
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
