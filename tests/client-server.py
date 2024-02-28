import socket
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
import os
import time
import sys
import traceback

from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWidgets import *

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


def generate_ecdh_key_pair():
    start = time.time()
    private_key = ec.generate_private_key(ec.SECP256R1(), default_backend())
    public_key = private_key.public_key()
    end = time.time()
    print(f"Time Taken: {end - start}")
    return private_key, public_key


def send_public_key(server_socket, public_key):
    serialized_key = public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )
    server_socket.send(serialized_key)


def key_exchange(server_socket):
    private_key, public_key = generate_ecdh_key_pair()
    send_public_key(server_socket, public_key)

    received_key = server_socket.recv(4096)
    peer_public_key = serialization.load_pem_public_key(received_key, backend=default_backend())
    shared_key = private_key.exchange(ec.ECDH(), peer_public_key)

    return shared_key


def encrypt_data(key, plaintext):
    nonce = os.urandom(12)
    cipher = AESGCM(key)
    ciphertext = cipher.encrypt(nonce, plaintext.encode(), None)
    return nonce + ciphertext


def decrypt_data(key, ciphertext):
    nonce = ciphertext[:12]
    ciphertext = ciphertext[12:]
    cipher = AESGCM(key)
    plaintext = cipher.decrypt(nonce, ciphertext, None)
    return plaintext.decode()


def send_data(ip, data):
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print(f"Connecting to {ip}")
    client.connect((ip, 26555))

    shared_key = key_exchange(client)

    encrypted_data = encrypt_data(shared_key, data)
    client.send(encrypted_data)
    encrypted_response = client.recv(4096)
    decrypted_response = decrypt_data(shared_key, encrypted_response)

    client.close()
    return (encrypted_response, decrypted_response)


# Create a simple GUI window with 2 fields and a button:
# IP field, send button, and a text field

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()

        self.setWindowTitle("Client")
        self.setGeometry(100, 100, 400, 200)

        layout = QVBoxLayout()

        self.ip_field = QLineEdit()
        self.ip_field.setPlaceholderText("IP Address")
        layout.addWidget(self.ip_field)

        self.send_button = QPushButton("Send")
        self.send_button.clicked.connect(self.send)
        layout.addWidget(self.send_button)

        self.text_field = QTextEdit()
        layout.addWidget(self.text_field)

        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)

    def send(self):
        ip = self.ip_field.text()
        data = self.text_field.toPlainText()

        worker = Worker(send_data, ip, data)  # Any other args, kwargs are passed to the run function
        worker.signals.result.connect(self.print_output)
        worker.signals.finished.connect(self.thread_complete)
        worker.signals.error.connect(self.print_err)

        # Execute
        QThreadPool.globalInstance().start(worker)

    def print_output(self, s):
        print(s)

    def print_err(self, s):
        print(s[1])

    def thread_complete(self):
        print("THREAD COMPLETE!")

app = QApplication([])
window = MainWindow()
window.show()

app.exec()