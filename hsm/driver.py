import socket
import traceback

from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from Crypto.Cipher import DES, DES3, Blowfish
from twofish import Twofish
from Crypto.Util.Padding import pad
import threading
import os
import hashlib
import sys
import sqlite3
import time
import subprocess
import psutil
import base64
import uuid
import random
import string
import rsa
from multiprocessing import Pool

valid_hashes = hashlib.algorithms_available
valid_encryption_decryption_algorithms = ["aes", "rsa", "des", "3des", "blowfish", "twofish"]
valid_secret_generators = ["uuid4", "random", "randomstring", "randomnumber"]


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
            "CREATE TABLE secrets (sid INTEGER PRIMARY KEY, uid INTEGER, label TEXT, secret TEXT, FOREIGN KEY(uid) REFERENCES users(uid))")
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
    # Check if the data fits the protocol. If it does, return True. Otherwise, return False.
    """
    1) The data must start with polaris://
    2) Data must be in the form of <action>:<data>
    3) The action must be a valid hash, encryption algorithm or secret generator.
    4) The final 3 values should be the machine identifier, the master password and the username.
    """
    if not data.startswith("polaris://"):
        return False

    data = data[10:]
    data = data.split("/")

    if len(data) != 4:
        print(f"[{time.ctime()}] Invalid data received: {data} | Does not have the correct number of elements.")
        return False

    # Replace the data[0] element with the lower of itself
    action = data[0].lower().split(":")[0]
    mid = data[1].split(":")[1]
    mp = data[2].split(":")[1]
    username = data[3].split(":")[1]

    if data[1].split(":")[0] != "mid" or data[2].split(":")[0] != "mp" or data[3].split(":")[0] != "username":
        print(f"[{time.ctime()}] Invalid data received: {data} | One or more elements are not in the correct format.")
        return False

    elif mid == "" or mp == "" or username == "":
        print(f"[{time.ctime()}] Invalid data received: {data} | One or more elements are empty.")
        return False

    elif action in valid_hashes or action in valid_encryption_decryption_algorithms or action in valid_secret_generators:
        print(f"[{time.ctime()}] Valid data received: {data}")
        return True
    return False


def protocol_handler(data, shared_key):
    data = data[10:]
    data = data.split(":")
    data[0] = data[0].lower()
    print(f"[{time.ctime()}] Protocol handler received: {data}")
    if data[0] in valid_hashes:
        h = hashlib.new(data[0])
        h.update(data[1].encode())
        data = "polaris://" + data[0] + ":" + h.hexdigest()
        return data
    elif data[0] in valid_encryption_decryption_algorithms:
        if data[0] == "aes":
            cipher = AESGCM(shared_key)
            nonce = os.urandom(12)
            ciphertext = cipher.encrypt(nonce, data[1].encode(), None)
            ciphertext_base64 = base64.b64encode(ciphertext).decode()
            nonce_base64 = base64.b64encode(nonce).decode()
            data = "polaris://" + data[0] + ":" + nonce_base64 + ":" + ciphertext_base64
            return data
        elif data[0] == "rsa":
            print(f"[{time.ctime()}] Generating RSA key pair, this may take a while...")
            (pub, priv) = rsa.newkeys(2048) # Poolsize omitted, daemonic process not allowed. THIS IS A FUTURE TODO!
            print(f"[{time.ctime()}] RSA key pair generated.")
            pub = base64.b64encode(pub.save_pkcs1()).decode()
            priv = base64.b64encode(priv.save_pkcs1()).decode()
            data = "polaris://" + data[0] + ":[pub]" + pub + ":[priv]" + priv
            return data
        elif data[0] == "des":
            cipher = DES.new(shared_key[:8], DES.MODE_ECB)
            data = "polaris://" + data[0] + ":" + base64.b64encode(cipher.encrypt(pad(data[1].encode(), 8))).decode()
            return data
        elif data[0] == "3des":
            cipher = DES3.new(shared_key[:24], DES3.MODE_ECB)
            data = "polaris://" + data[0] + ":" + base64.b64encode(cipher.encrypt(pad(data[1].encode(), 8))).decode()
            return data
        elif data[0] == "blowfish":
            cipher = Blowfish.new(shared_key[:16], Blowfish.MODE_ECB)
            data = "polaris://" + data[0] + ":" + base64.b64encode(cipher.encrypt(pad(data[1].encode(), 8))).decode()
            return data
        elif data[0] == "twofish":
            cipher = Twofish(shared_key[:32])
            ciphertext = b""
            if len(data[1]) % 16 != 0:
                # Pad it
                data[1] = data[1] + " " * (16 - len(data[1]) % 16)
            for i in range(0, len(data[1]), 16):
                ciphertext += cipher.encrypt(data[1][i:i + 16].encode())
            data = "polaris://" + data[0] + ":" + base64.b64encode(ciphertext).decode()
            return data

    elif data[0] in valid_secret_generators:
        if data[0] == "uuid4":
            data = "polaris://" + data[0] + ":" + str(uuid.uuid4())
            return data
        elif data[0] == "random":
            data = "polaris://" + data[0] + ":" + str(os.urandom(16))
            return data
        elif data[0] == "randomstring":
            data = "polaris://" + data[0] + ":" + ''.join(random.choices(string.ascii_letters + string.digits, k=16))
            return data
        elif data[0] == "randomnumber":
            data = "polaris://" + data[0] + ":" + str(random.randint(0, 100))
            return data

    elif data[0] == "store":
        logger("Store command received.")
    elif data[0] == "retrieve":
        logger("Retrieve command received.")


def handle_client(client_socket):
    shared_key = key_exchange(client_socket)
    encrypted_data = client_socket.recv(8192)
    if len(encrypted_data) == 0:
        print(f"[{time.ctime()}] Connection closed by {client_socket.getpeername()}")
        logger(f"Connection closed by {client_socket.getpeername()}")
        client_socket.close()
        return
    decrypted_data = decrypt_data(shared_key, encrypted_data)

    # Process the decrypted_data as needed
    print(f"[{time.ctime()}] Received encrypted data: {encrypted_data}")
    logger(f"Received encrypted data: {encrypted_data} from {client_socket.getpeername()}")
    sys.stdout.flush()  # Journalctl Prints
    print(f"[{time.ctime()}] Decrypted data: {decrypted_data}")
    logger(f"Decrypted data: {decrypted_data}")
    sys.stdout.flush()  # Journalctl Prints

    if decrypted_data == "Hello, HSM":
        print(f"[{time.ctime()}] This looks like a handshake.")
        logger(f"This looks like a handshake.")
        encrypted_data = encrypt_data(shared_key, "Hello, Client")
        client_socket.send(encrypted_data)
        print(f"[{time.ctime()}] Sent encrypted data: Hello, Client")
        logger(f"Sent encrypted data: Hello, Client to {client_socket.getpeername()}")
        sys.stdout.flush()  # Journalctl Prints
        client_socket.close()
        return

    elif decrypted_data.startswith("polaris://mid:") and len(
            decrypted_data.replace("polaris://", "").split("/")) == 3:
        print(f"[{time.ctime()}] Client has initiated setup.")
        logger(f"Client has initiated setup.")
        mid = decrypted_data.replace("polaris://mid:", "").split("/")[0]
        mp = decrypted_data.replace("polaris://mid:", "").split("/")[1]
        username = decrypted_data.replace("polaris://mid:", "").split("/")[2]
        print(f"[{time.ctime()}] Received: {mid}, {mp}, {username}")
        logger(f"Received: {mid}, {mp}, {username} from {client_socket.getpeername()}")
        sys.stdout.flush()  # Journalctl Prints
        # Check if this combination of username, password and machine id already exists in the database
        # Check if the MID and IP combination already exists in the database as well
        try:
            conn = sqlite3.connect("/etc/polaris/polaris.db")
            c = conn.cursor()
            salt = open("/etc/polaris/salt", "r").read()
            users_combo = c.execute("SELECT * FROM users WHERE username = ? AND password = ? AND mid = ?", (username, hashlib.sha256((mp + salt).encode()).hexdigest(), mid)).fetchall()
            machines_combo = c.execute("SELECT * FROM machines WHERE mid = ? AND ip = ?", (mid, client_socket.getpeername()[0])).fetchall()
            if len(users_combo) > 0 or len(machines_combo) > 0:
                encrypted_data = encrypt_data(shared_key, "polaris://mid:failure")
                client_socket.send(encrypted_data)
                print(f"[{time.ctime()}] Sent encrypted data: polaris://mid:failure")
                logger(f"Sent encrypted data: polaris://mid:failure to {client_socket.getpeername()}")
                sys.stdout.flush()
                client_socket.close()
                return
            c.execute("INSERT INTO machines (mid, ip) VALUES (?, ?)", (mid, client_socket.getpeername()[0]))
            mp_hash = hashlib.sha256((mp + salt).encode()).hexdigest()
            c.execute("INSERT INTO users (username, password, mid) VALUES (?, ?, ?)", (username, mp_hash, mid))
            conn.commit()
            encrypted_data = encrypt_data(shared_key, "polaris://mid:success")
            client_socket.send(encrypted_data)
            print(f"[{time.ctime()}] Sent encrypted data: polaris://mid:success")
            logger(f"Sent encrypted data: polaris://mid:success to {client_socket.getpeername()}")
            sys.stdout.flush()  # Journalctl Prints
        except sqlite3.IntegrityError:
            encrypted_data = encrypt_data(shared_key, "polaris://mid:failure")
            client_socket.send(encrypted_data)
            print(f"[{time.ctime()}] Sent encrypted data: polaris://mid:failure")
            logger(f"Sent encrypted data: polaris://mid:failure to {client_socket.getpeername()}")
            sys.stdout.flush()
        client_socket.close()
        return

    elif protocol(decrypted_data):
        print(f"[{time.ctime()}] Protocol validation successful: {decrypted_data}")
        logger(f"Protocol validation successful: {decrypted_data}")
        data_to_return = protocol_handler(decrypted_data, shared_key)
        encrypted_data = encrypt_data(shared_key, data_to_return)
        print(f"[{time.ctime()}] Sending encrypted data: {encrypted_data}")
        client_socket.send(encrypted_data)
        print(f"[{time.ctime()}] Sent encrypted data: {data_to_return}")
        logger(f"Sent encrypted data: {data_to_return} to {client_socket.getpeername()}")
        sys.stdout.flush()  # Journalctl Prints
        return

    else:
        print(f"[{time.ctime()}] Invalid data received: {decrypted_data}")
        logger(f"Invalid data received: {decrypted_data}")
        encrypted_data = encrypt_data(shared_key, "polaris://error")
        client_socket.send(encrypted_data)
        print(f"[{time.ctime()}] Sent encrypted data: polaris://error")
        logger(f"Sent encrypted data: polaris://error to {client_socket.getpeername()}")
        sys.stdout.flush()
        client_socket.close()
        return


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
                print(f"[{time.ctime()}] Connection closed by {client_socket.getpeername()}")
                sys.stdout.flush()  # Journalctl Prints
                client_socket.close()
                return
            except OSError:
                print(f"[{time.ctime()}] Connection closed by previously connected client.")
                sys.stdout.flush()  # Journalctl Prints
                client_socket.close()
                return
        time.sleep(1)


def start_server():
    try:
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
    except KeyboardInterrupt:
        print(f"[{time.ctime()}] Server stopped by the user.")
        sys.stdout.flush()
        logger(f"Server stopped by the user.")
        server.close()
        sys.exit(0)
    except Exception as e:
        print(f"[{time.ctime()}] An error occurred: {e}")
        sys.stdout.flush()
        logger(f"An error occurred: {e}")
        logger(traceback.format_exc())


def start_statistics_server():
    try:
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
    except KeyboardInterrupt:
        print(f"[{time.ctime()}] Statistics Server stopped by the user.")
        sys.stdout.flush()
        logger(f"Statistics Server stopped by the user.")
        server.close()
        sys.exit(0)
    except Exception as e:
        print(f"[{time.ctime()}] An error occurred: {e}")
        sys.stdout.flush()
        logger(f"An error occurred: {e}")
        logger(traceback.format_exc())


def muted_initializer():
    sys.stderr = open(os.devnull, "w")


if __name__ == '__main__':
    db_exists = check_if_db_exists()
    log_exists = check_if_log_exists()
    pool = None
    if not db_exists:
        logger(f"Database not found. Creating a new database...")
    else:
        logger(f"Database found. Continuing with the existing database...")
    try:
        with Pool() as pool:
            pool.apply_async(start_server)
            pool.apply_async(start_statistics_server)
            while True:
                time.sleep(1)
    except KeyboardInterrupt:
        print(f"[{time.ctime()}] Server stopped by the user.")
        sys.stdout.flush()
        logger(f"Server stopped by the user.")
        if pool:
            # Kill all threads in the pool and hard exit
            pool.terminate()
            pool.join()
        sys.exit(0)
    except Exception as e:
        print(f"[{time.ctime()}] An error occurred: {e}")
        sys.stdout.flush()
        logger(f"An error occurred: {e}")
        logger(traceback.format_exc())
