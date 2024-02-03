import timeit
import socket


def connect_to_hsm(ip_address):
    # Try connecting to HSM for 5 seconds - if not, timeout, return "Connection failed"
    try:
        # Connect to HSM
        hsm = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        hsm.settimeout(5)
        hsm.connect((ip_address, 26555))
        hsm.send(b'Hello, HSM')
        data = hsm.recv(1024)
        hsm.close()
        print(data)
    except TimeoutError:
        raise Exception("Connection to HSM timed out")
    except socket.error:
        raise Exception("Connection to HSM failed")
