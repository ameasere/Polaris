import unittest
import timeit
from multiprocessing import Pool
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa
import subprocess

def generate_key_cryptography(thread_number):
    start = timeit.default_timer()
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=4096,
        backend=default_backend()
    )
    pem = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption()
    )

    # generate public key
    public_key = private_key.public_key()
    pem2 = public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )
    stop = timeit.default_timer()
    return f'Thread {thread_number} Time (cryptography): ', (stop - start) * 1000  # convert to milliseconds

def generate_key_subprocess(thread_number):
    cmd = "openssl genrsa 2048"
    start = timeit.default_timer()
    process = subprocess.Popen(cmd.split(), stdout=subprocess.PIPE, shell=True)
    output, error = process.communicate()
    stop = timeit.default_timer()
    return f'Thread {thread_number} Time (subprocess): ', (stop - start) * 1000  # convert to milliseconds

class TestKeyGeneration(unittest.TestCase):
    def test_key_generation(self):
        with Pool() as p:
            cryptography_results = p.map(generate_key_cryptography, range(1, 51))  # replace 3 with the number of processes you want to create
            subprocess_results = p.map(generate_key_subprocess, range(1, 51))  # replace 3 with the number of processes you want to create
            # Example out: [('Thread 1 Time (cryptography): ', 547.8900830000001), ('Thread 2 Time (cryptography): ', 715.068917), ('Thread 3 Time (cryptography): ', 806.410708)]
            # Print average time across all threads
            print("Average time (cryptography): ", sum([x[1] for x in cryptography_results]) / len(cryptography_results), "ms")
            print("Average time (subprocess): ", sum([x[1] for x in subprocess_results]) / len(subprocess_results), "ms")
if __name__ == '__main__':
    unittest.main()