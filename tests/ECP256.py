import unittest
import multiprocessing
import time
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import ec


def worker(thread_number):
    start = time.time()
    private_key = ec.generate_private_key(ec.SECP256R1(), default_backend())
    public_key = private_key.public_key()
    end = time.time()
    return end - start


class TestECDHKeyPairGeneration(unittest.TestCase):
    def test_average_time(self):
        with multiprocessing.Pool() as p:
            ecresults = p.map(worker, range(20))
        print("Average time: ", sum([x for x in ecresults]) / len(ecresults), "ms")


if __name__ == '__main__':
    unittest.main()
