import socket
import traceback

from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
import threading
import os
import hashlib
import sys
import sqlite3
import time
import subprocess
import psutil
from multiprocessing import Process


def check_if_db_exists():
    if not os.path.exists("/etc/polaris/polaris.db"):
        print(f"[{time.ctime()}] Database not found. Creating a new database...")
        sys.stdout.flush()
        logger("Database not found. Creating a new database...")
        conn = sqlite3.connect("/etc/polaris/polaris.db")
        c = conn.cursor()
        c.execute("CREATE TABLE machines (mid TEXT PRIMARY KEY, ip TEXT)")
        c.execute(
            "CREATE TABLE users (uid INTEGER PRIMARY KEY, username TEXT, password TEXT, mid INTEGER, FOREIGN KEY(mid) REFERENCES machines(mid))")
        c.execute(
            "CREATE TABLE secrets (sid INTEGER PRIMARY KEY, uid INTEGER, secret TEXT, FOREIGN KEY(uid) REFERENCES users(uid))")
        conn.commit()
        conn.close()
        return False
    else:
        print(f"[{time.ctime()}] Database found. Continuing with the existing database...")
        sys.stdout.flush()
        logger("Database found. Continuing with the existing database...")
        return True


def check_if_log_exists():
    if not os.path.exists("/var/log/polaris.log"):
        print(f"[{time.ctime()}] Log file not found. Creating a new log file...")
        sys.stdout.flush()
        subprocess.run(["touch", "/var/log/polaris.log"])
        subprocess.run(["chown", "polaris:polaris", "/var/log/polaris.log"])
        subprocess.run(["chmod", "640", "/var/log/polaris.log"])
        subprocess.run(["systemctl", "restart", "rsyslog"])
        logger("Log file not found. Creating a new log file...")
        return False
    else:
        print(f"[{time.ctime()}] Log file found. Continuing with the existing log file...")
        sys.stdout.flush()
        logger("Log file found. Continuing with the existing log file...")
        return True


def logger(message):
    now = time.ctime()
    open("/var/log/polaris.log", "a").write(f"[{now}] {message}\n")


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


def protocol(data):
    pass


def protocol_handler(data, client_socket, shared_key):
    pass


def handle_client(client_socket):
    shared_key = key_exchange(client_socket)
    encrypted_data = client_socket.recv(1024)
    if len(encrypted_data) == 0:
        print(f"Connection closed by {client_socket.getpeername()}")
        logger(f"Connection closed by {client_socket.getpeername()}")
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
        logger(f"Sent encrypted data: Hello, Client to {client_socket.getpeername()}")
        sys.stdout.flush()  # Journalctl Prints
        client_socket.close()
        return

    elif decrypted_data.startswith("polaris://mid:") and len(
            decrypted_data.replace("polaris://", "").split("/")) == 3:
        mid = decrypted_data.replace("polaris://mid:", "").split("/")[0]
        mp = decrypted_data.replace("polaris://mid:", "").split("/")[1]
        username = decrypted_data.replace("polaris://mid:", "").split("/")[2]
        print(f"Received: {mid}, {mp}, {username}")
        logger(f"Received: {mid}, {mp}, {username} from {client_socket.getpeername()}")
        sys.stdout.flush()  # Journalctl Prints
        try:
            conn = sqlite3.connect("/etc/polaris/polaris.db")
            c = conn.cursor()
            c.execute("SELECT * FROM machines WHERE mid=?", (mid,))
            c.execute("INSERT INTO machines (mid, ip) VALUES (?, ?)", (mid, client_socket.getpeername()[0]))
            salt = open("/etc/polaris/salt", "r").read()
            mp_hash = hashlib.sha256((mp + salt).encode()).hexdigest()
            c.execute("INSERT INTO users (username, password, mid) VALUES (?, ?, ?)", (username, mp_hash, mid))
            conn.commit()
            encrypted_data = encrypt_data(shared_key, "polaris://mid:success")
            client_socket.send(encrypted_data)
            print("Sent encrypted data: polaris://mid:success")
            logger(f"Sent encrypted data: polaris://mid:success to {client_socket.getpeername()}")
            sys.stdout.flush()  # Journalctl Prints
        except sqlite3.IntegrityError:
            encrypted_data = encrypt_data(shared_key, "polaris://mid:failure")
            client_socket.send(encrypted_data)
            print("Sent encrypted data: polaris://mid:failure")
            logger(f"Sent encrypted data: polaris://mid:failure to {client_socket.getpeername()}")
            sys.stdout.flush()
        client_socket.close()
        return

    elif protocol(decrypted_data):
        protocol_handler(decrypted_data, client_socket, shared_key)
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


def handle_statistics_client(client_socket):
    # Send statistics data every second
    while True:
        cpu_percent = psutil.cpu_percent()
        if "coretemp" in psutil.sensors_temperatures():
            gpu_percent = psutil.sensors_temperatures()["coretemp"][0].current
        else:
            gpu_percent = 0
        ram_percent = psutil.virtual_memory().percent
        disk_percent = psutil.disk_usage("/").percent
        data = f"polaris://cpu:{cpu_percent}/gpu:{gpu_percent}/ram:{ram_percent}/disk:{disk_percent}"
        try:
            client_socket.send(data.encode())
        except ConnectionResetError:
            try:
                print(f"{time.ctime()} Connection closed by {client_socket.getpeername()}")
                sys.stdout.flush()  # Journalctl Prints
                client_socket.close()
                return
            except OSError:
                print(f"{time.ctime()} Connection closed by previously connected client.")
                sys.stdout.flush()  # Journalctl Prints
                client_socket.close()
                return
        time.sleep(1)


def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('0.0.0.0', 26555))
    server.listen(5)

    print(f"[{time.ctime()}] Server listening on port 26555")
    logger(f"Server listening on port 26555")
    sys.stdout.flush()  # Journalctl Prints

    while True:
        client_socket, addr = server.accept()
        print(f"[{time.ctime()}] Accepted connection from {addr}")
        sys.stdout.flush()  # Journalctl Prints
        client_handler = threading.Thread(target=handle_client, args=(client_socket,))
        client_handler.start()


def start_statistics_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('0.0.0.0', 26556))
    server.listen(5)

    print(f"[{time.ctime()}] Statistics Server listening on port 26556")
    logger(f"Statistics Server listening on port 26556")
    sys.stdout.flush()  # Journalctl Prints

    while True:
        client_socket, addr = server.accept()
        print(f"[{time.ctime()}] Accepted connection from {addr}")
        sys.stdout.flush()
        client_handler = threading.Thread(target=handle_statistics_client, args=(client_socket,))
        client_handler.start()


if __name__ == '__main__':
    db_exists = check_if_db_exists()
    log_exists = check_if_log_exists()
    if not db_exists:
        logger(f"Database not found. Creating a new database...")
    else:
        logger(f"Database found. Continuing with the existing database...")
    try:
        server_process = Process(target=start_server)
        server_process.start()
        statistics_server_process = Process(target=start_statistics_server)
        statistics_server_process.start()
    except KeyboardInterrupt:
        print(f"[{time.ctime()}] Server stopped by the user.")
        sys.stdout.flush()
        logger(f"Server stopped by the user.")
    except Exception as e:
        print(f"[{time.ctime()}] An error occurred: {e}")
        sys.stdout.flush()
        logger(f"An error occurred: {e}")
        logger(traceback.format_exc())
