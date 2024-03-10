import socket
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
import os
import time
import sys
import traceback


def generate_ecdh_key_pair():
    private_key = ec.generate_private_key(ec.SECP256R1(), default_backend())
    public_key = private_key.public_key()
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


def connector(ip_address):
    hsm = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    hsm.settimeout(5)
    hsm.connect((ip_address, 26555))
    return hsm


def statistics_connector(ip_address):
    hsm = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    hsm.settimeout(5)
    hsm.connect((ip_address, 26556))
    return hsm


def ping_hsm(ip_address):
    try:
        hsm = connector(ip_address)
        handshake_key = key_exchange(hsm)
        handshake = encrypt_data(handshake_key, "Hello, HSM")
        hsm.send(handshake)
        data = hsm.recv(1024)
        decrypted_data = decrypt_data(handshake_key, data)
        hsm.close()
        if decrypted_data != "Hello, Client":
            raise Exception("Handshake failed")
        else:
            return True
    except TimeoutError:
        raise Exception("Connection to HSM timed out")
    except socket.error:
        raise Exception("Connection to HSM failed")


def connect_to_hsm_post_setup(ip_address, machine_identifier, master_password, username, action_string):
    try:
        hsm = connector(ip_address)
        handshake_key = key_exchange(hsm)
        handshake = encrypt_data(handshake_key, "Hello, HSM")
        hsm.send(handshake)
        data = hsm.recv(1024)
        decrypted_data = decrypt_data(handshake_key, data)
        hsm.close()
        if decrypted_data != "Hello, Client":
            raise Exception("Handshake failed")
        else:
            hsm = connector(ip_address)
            handshake_key = key_exchange(hsm)
            encrypted_setup = encrypt_data(handshake_key, action_string)
            hsm.send(encrypted_setup)
            response = hsm.recv(1024)
            decrypted_response = decrypt_data(handshake_key, response)
            hsm.close()
            return decrypted_response
    except TimeoutError:
        raise Exception("Connection to HSM timed out")
    except socket.error:
        raise Exception("Connection to HSM failed")


def connect_to_hsm_setup(ip_address, machine_identifier, master_password, username):
    # Try connecting to HSM for 5 seconds - if not, timeout, return "Connection failed"
    try:
        # Connect to HSM
        hsm = connector(ip_address)
        handshake_key = key_exchange(hsm)
        handshake = encrypt_data(handshake_key, "Hello, HSM")
        hsm.send(handshake)
        data = hsm.recv(1024)
        decrypted_data = decrypt_data(handshake_key, data)
        hsm.close()
        if decrypted_data != "Hello, Client":
            raise Exception("Handshake failed")
        else:
            hsm = connector(ip_address)
            handshake_key = key_exchange(hsm)
            initial_setup = f"polaris://mid:{machine_identifier}/mp:{master_password}/username:{username}"
            encrypted_setup = encrypt_data(handshake_key, initial_setup)
            hsm.send(encrypted_setup)
            response = hsm.recv(1024)
            decrypted_response = decrypt_data(handshake_key, response)
            hsm.close()
            return decrypted_response
    except TimeoutError:
        raise Exception("Connection to HSM timed out")
    except socket.error:
        raise Exception("Connection to HSM failed")
