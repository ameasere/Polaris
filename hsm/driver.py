import socket
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
import threading
import os
import hashlib


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


def handle_client(client_socket):
    shared_key = key_exchange(client_socket)

    encrypted_data = client_socket.recv(1024)
    decrypted_data = decrypt_data(shared_key, encrypted_data)

    # Process the decrypted_data as needed
    print(f"Received encrypted data: {encrypted_data}")
    print(f"Decrypted data: {decrypted_data}")

    if decrypted_data == "Hello, HSM":
        encrypted_data = encrypt_data(shared_key, "Hello, Client")
        client_socket.send(encrypted_data)
        print("Sent encrypted data: Hello, Client")
        client_socket.close()
        return

    if not decrypted_data.startswith("polaris://"):
        print("Invalid data received")
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
        return

    data = "polaris://" + action + ":" + data
    encrypted_data = encrypt_data(shared_key, data)

    client_socket.send(encrypted_data)
    print(f"Sent encrypted data: polaris://{action}:{old_data}")

    client_socket.close()


def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('0.0.0.0', 26555))
    server.listen(5)

    print("Server listening on port 26555")

    while True:
        client_socket, addr = server.accept()
        print(f"Accepted connection from {addr}")
        client_handler = threading.Thread(target=handle_client, args=(client_socket,))
        client_handler.start()


if __name__ == '__main__':
    start_server()
