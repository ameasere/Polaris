import socket
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
import threading
import os
import hashlib
import sys
import subprocess
import sqlite3
import time


def check_if_db_exists():
    if not os.path.exists("/etc/polaris/polaris.db"):
        conn = sqlite3.connect("/etc/polaris/polaris.db")
        c = conn.cursor()
        c.execute(
            "CREATE TABLE machines (mid INTEGER PRIMARY KEY, ip TEXT, name TEXT)")
        c.execute(
            "CREATE TABLE users (uid INTEGER PRIMARY KEY, username TEXT, password TEXT, mid INTEGER, FOREIGN KEY(mid) REFERENCES machines(mid))")
        c.execute(
            "CREATE TABLE secrets (sid INTEGER PRIMARY KEY, uid INTEGER, secret TEXT, FOREIGN KEY(uid) REFERENCES users(uid))")
        conn.commit()
        conn.close()
        return False
    else:
        return True


def check_if_log_exists():
    now = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    if not os.path.exists("/var/log/polaris.log"):
        subprocess.run(["touch", "/var/log/polaris.log"])
        subprocess.run(["chown", "polaris:polaris", "/var/log/polaris.log"])
        subprocess.run(["chmod", "640", "/var/log/polaris.log"])
        subprocess.run(["systemctl", "restart", "rsyslog"])
        open("/var/log/polaris.log", "w").write(f"[{now}] Log file created\n")
        return False
    else:
        open("/var/log/polaris.log", "a").write(f"[{now}] Log file found\n")
        return True


def generate_ecdh_key_pair():
    private_key = ec.generate_private_key(ec.SECP256R1(), default_backend())
    public_key = private_key.public_key()
    return private_key, public_key


def send_public_key(client_socket, public_key):
    serialized_key = public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )
    client_socket.send(serialized_key)


def key_exchange(client_socket):
    private_key, public_key = generate_ecdh_key_pair()
    send_public_key(client_socket, public_key)

    received_key = client_socket.recv(4096)
    peer_public_key = serialization.load_pem_public_key(
        received_key, backend=default_backend())
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


def handle_client(client_socket, c):
    shared_key = key_exchange(client_socket)
    while True:
        encrypted_data = client_socket.recv(1024)
        if len(encrypted_data) == 0:
            print(f"Connection closed by {client_socket.getpeername()}")
            client_socket.close()
            return
        decrypted_data = decrypt_data(shared_key, encrypted_data)

        # Process the decrypted_data as needed
        print(f"Received encrypted data: {encrypted_data}")
        sys.stdout.flush()  # Journalctl Prints
        print(f"Decrypted data: {decrypted_data}")
        sys.stdout.flush()  # Journalctl Prints

        if decrypted_data == "Hello, HSM":
            encrypted_data = encrypt_data(shared_key, "Hello, Client")
            client_socket.send(encrypted_data)
            print("Sent encrypted data: Hello, Client")
            sys.stdout.flush()  # Journalctl Prints
            client_socket.close()
            return

        if not decrypted_data.startswith("polaris://"):
            print("Invalid data received")
            sys.stdout.flush()  # Journalctl Prints
            return

        # Remove the "polaris://" prefix
        decrypted_data = decrypted_data[10:]
        # Form of <action>:<data>
        decrypted_data = decrypted_data.split(":")
        action = decrypted_data[0]
        if len(decrypted_data) > 1:
            data = decrypted_data[1]
        if action in hashlib.algorithms_available:
            h = hashlib.new(action)
            h.update(data.encode())
            data = h.hexdigest()
            old_data = data
        else:
            print("Invalid action received")
            sys.stdout.flush()  # Journalctl Prints
            return

        data = "polaris://" + action + ":" + data
        encrypted_data = encrypt_data(shared_key, data)

        client_socket.send(encrypted_data)
        print(f"Sent encrypted data: polaris://{action}:{old_data}")
        sys.stdout.flush()  # Journalctl Prints

        # client_socket.close()


def start_server(c):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('0.0.0.0', 26555))
    server.listen(5)

    print("Server listening on port 26555")
    sys.stdout.flush()  # Journalctl Prints

    while True:
        client_socket, addr = server.accept()
        print(f"Accepted connection from {addr}")
        sys.stdout.flush()  # Journalctl Prints
        client_handler = threading.Thread(
            target=handle_client, args=(
                client_socket, c))
        client_handler.start()


if __name__ == '__main__':
    db_exists = check_if_db_exists()
    log_exists = check_if_log_exists()
    now = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    if not db_exists:
        open(
            "/var/log/polaris.log",
            "w").write(f"[{now}] Database was not found. Creating a new one...\n")
    else:
        open(
            "/var/log/polaris.log",
            "w").write(f"[{now}] Database found. Continuing...\n")
    conn = sqlite3.connect("/etc/polaris/polaris.db")
    c = conn.cursor()
    start_server(c)
