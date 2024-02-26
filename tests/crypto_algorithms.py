# Test which cryptographic algorithms are viable in both single and
# multi-threaded environments.

from Cryptodome.Cipher import AES, Blowfish
from Cryptodome.Hash import SHA256, SHA384, SHA512, HMAC
from Cryptodome.Util import Padding
import threading
import time
import colorama
import psutil
import rsa

test_string = b"Hello, world!"
test_key = b"1234567890123456"
# 16 byte IV
test_iv = b"1234567890123456"

rsa_string_to_sign = bytes("A" * 1024, encoding="utf-8")


# Time each algorithm
def test_aes():
    start_time = time.time()

    cipher = AES.new(test_key, AES.MODE_CBC, test_iv)
    cipher.encrypt(Padding.pad(test_string, 16))

    end_time = time.time()
    end_cpu_usage = psutil.cpu_percent(
        interval=0.1)  # Adjust interval as needed

    print(colorama.Fore.GREEN + "[AES] Duration: " + colorama.Fore.BLUE + str(
        end_time - start_time) + colorama.Fore.RESET)
    print(
        colorama.Fore.YELLOW +
        "[AES] CPU Usage: " +
        colorama.Fore.CYAN +
        f"{end_cpu_usage:.2f}%" +
        colorama.Fore.RESET)
    return end_time - start_time


def test_blowfish():
    start = time.time()
    cipher = Blowfish.new(test_key, Blowfish.MODE_CBC, test_iv[:8])
    cipher.encrypt(Padding.pad(test_string, 8))
    end = time.time()
    end_cpu_usage = psutil.cpu_percent(
        interval=0.1)  # Adjust interval as needed
    print(colorama.Fore.GREEN +
          "[Blowfish] Duration: " +
          colorama.Fore.BLUE +
          str(end -
              start) +
          colorama.Fore.RESET)
    print(
        colorama.Fore.YELLOW +
        "[Blowfish] CPU Usage: " +
        colorama.Fore.CYAN +
        f"{end_cpu_usage:.2f}%" +
        colorama.Fore.RESET)
    return end - start


def test_sha256():
    start = time.time()
    hsh = SHA256.new()
    hsh.update(test_string)
    hsh.digest()
    end = time.time()
    end_cpu_usage = psutil.cpu_percent(
        interval=0.1)  # Adjust interval as needed
    print(colorama.Fore.GREEN +
          "[SHA256] Duration: " +
          colorama.Fore.BLUE +
          str(end -
              start) +
          colorama.Fore.RESET)
    print(
        colorama.Fore.YELLOW +
        "[SHA256] CPU Usage: " +
        colorama.Fore.CYAN +
        f"{end_cpu_usage:.2f}%" +
        colorama.Fore.RESET)
    return end - start


def test_sha384():
    start = time.time()
    hsh = SHA384.new()
    hsh.update(test_string)
    hsh.digest()
    end = time.time()
    end_cpu_usage = psutil.cpu_percent(
        interval=0.1)  # Adjust interval as needed
    print(colorama.Fore.GREEN +
          "[SHA384] Duration: " +
          colorama.Fore.BLUE +
          str(end -
              start) +
          colorama.Fore.RESET)
    print(
        colorama.Fore.YELLOW +
        "[SHA384] CPU Usage: " +
        colorama.Fore.CYAN +
        f"{end_cpu_usage:.2f}%" +
        colorama.Fore.RESET)
    return end - start


def test_sha512():
    start = time.time()
    hsh = SHA512.new()
    hsh.update(test_string)
    hsh.digest()
    end = time.time()
    end_cpu_usage = psutil.cpu_percent(
        interval=0.1)  # Adjust interval as needed
    print(colorama.Fore.GREEN +
          "[SHA512] Duration: " +
          colorama.Fore.BLUE +
          str(end -
              start) +
          colorama.Fore.RESET)
    print(
        colorama.Fore.YELLOW +
        "[SHA512] CPU Usage: " +
        colorama.Fore.CYAN +
        f"{end_cpu_usage:.2f}%" +
        colorama.Fore.RESET)
    return end - start


def test_hmac():
    start = time.time()
    hsh = HMAC.new(test_key)
    hsh.update(test_string)
    hsh.digest()
    end = time.time()
    end_cpu_usage = psutil.cpu_percent(
        interval=0.1)  # Adjust interval as needed
    print(colorama.Fore.GREEN +
          "[HMAC] Duration: " +
          colorama.Fore.BLUE +
          str(end -
              start) +
          colorama.Fore.RESET)
    print(
        colorama.Fore.YELLOW +
        "[HMAC] CPU Usage: " +
        colorama.Fore.CYAN +
        f"{end_cpu_usage:.2f}%" +
        colorama.Fore.RESET)
    return end - start


def rsa_varied_key_size_st():
    # 512, 1024, 2048, 4096
    start = time.time()
    key = rsa.newkeys(512)
    # Sign the message
    signature = rsa.sign(test_string, key[1], "SHA-256")
    end = time.time()
    end_cpu_usage = psutil.cpu_percent(
        interval=0.1)  # Adjust interval as needed
    print(colorama.Fore.GREEN +
          "[RSA 512] Duration: " +
          colorama.Fore.BLUE +
          str(end -
              start) +
          colorama.Fore.RESET)
    print(
        colorama.Fore.YELLOW +
        "[RSA 512] CPU Usage: " +
        colorama.Fore.CYAN +
        f"{end_cpu_usage:.2f}%" +
        colorama.Fore.RESET)

    start = time.time()
    key = rsa.newkeys(1024)
    # Sign the message
    signature = rsa.sign(test_string, key[1], "SHA-256")

    end = time.time()
    end_cpu_usage = psutil.cpu_percent(
        interval=0.1)  # Adjust interval as needed
    print(colorama.Fore.GREEN +
          "[RSA 1024] Duration: " +
          colorama.Fore.BLUE +
          str(end -
              start) +
          colorama.Fore.RESET)
    print(
        colorama.Fore.YELLOW +
        "[RSA 1024] CPU Usage: " +
        colorama.Fore.CYAN +
        f"{end_cpu_usage:.2f}%" +
        colorama.Fore.RESET)

    start = time.time()
    key = rsa.newkeys(2048)
    # Sign the message
    signature = rsa.sign(test_string, key[1], "SHA-256")

    end = time.time()
    end_cpu_usage = psutil.cpu_percent(
        interval=0.1)  # Adjust interval as needed
    print(colorama.Fore.GREEN +
          "[RSA 2048] Duration: " +
          colorama.Fore.BLUE +
          str(end -
              start) +
          colorama.Fore.RESET)
    print(
        colorama.Fore.YELLOW +
        "[RSA 2048] CPU Usage: " +
        colorama.Fore.CYAN +
        f"{end_cpu_usage:.2f}%" +
        colorama.Fore.RESET)

    start = time.time()
    key = rsa.newkeys(4096)
    # Sign the message
    signature = rsa.sign(test_string, key[1], "SHA-256")

    end = time.time()
    end_cpu_usage = psutil.cpu_percent(
        interval=0.1)  # Adjust interval as needed
    print(colorama.Fore.GREEN +
          "[RSA 4096] Duration: " +
          colorama.Fore.BLUE +
          str(end -
              start) +
          colorama.Fore.RESET)
    print(
        colorama.Fore.YELLOW +
        "[RSA 4096] CPU Usage: " +
        colorama.Fore.CYAN +
        f"{end_cpu_usage:.2f}%" +
        colorama.Fore.RESET)

    return end - start


def rsa_varied_key_size_mt():
    start = time.time()
    key = rsa.newkeys(512, poolsize=int(psutil.cpu_count()) - 2)
    # Sign the message
    signature = rsa.sign(test_string, key[1], "SHA-256")

    end = time.time()
    end_cpu_usage = psutil.cpu_percent(
        interval=0.1)  # Adjust interval as needed
    print(colorama.Fore.GREEN +
          "[RSA 512] Duration: " +
          colorama.Fore.BLUE +
          str(end -
              start) +
          colorama.Fore.RESET)
    print(
        colorama.Fore.YELLOW +
        "[RSA 512] CPU Usage: " +
        colorama.Fore.CYAN +
        f"{end_cpu_usage:.2f}%" +
        colorama.Fore.RESET)

    start = time.time()
    key = rsa.newkeys(1024, poolsize=int(psutil.cpu_count()) - 2)
    # Sign the message
    signature = rsa.sign(test_string, key[1], "SHA-256")

    end = time.time()
    end_cpu_usage = psutil.cpu_percent(
        interval=0.1)  # Adjust interval as needed
    print(colorama.Fore.GREEN +
          "[RSA 1024] Duration: " +
          colorama.Fore.BLUE +
          str(end -
              start) +
          colorama.Fore.RESET)
    print(
        colorama.Fore.YELLOW +
        "[RSA 1024] CPU Usage: " +
        colorama.Fore.CYAN +
        f"{end_cpu_usage:.2f}%" +
        colorama.Fore.RESET)

    start = time.time()
    key = rsa.newkeys(2048, poolsize=int(psutil.cpu_count()) - 2)
    # Sign the message
    signature = rsa.sign(test_string, key[1], "SHA-256")

    end = time.time()
    end_cpu_usage = psutil.cpu_percent(
        interval=0.1)  # Adjust interval as needed
    print(colorama.Fore.GREEN +
          "[RSA 2048] Duration: " +
          colorama.Fore.BLUE +
          str(end -
              start) +
          colorama.Fore.RESET)
    print(
        colorama.Fore.YELLOW +
        "[RSA 2048] CPU Usage: " +
        colorama.Fore.CYAN +
        f"{end_cpu_usage:.2f}%" +
        colorama.Fore.RESET)

    start = time.time()
    key = rsa.newkeys(4096, poolsize=int(psutil.cpu_count()) - 2)
    # Sign the message
    signature = rsa.sign(test_string, key[1], "SHA-256")

    end = time.time()
    end_cpu_usage = psutil.cpu_percent(
        interval=0.1)  # Adjust interval as needed
    print(colorama.Fore.GREEN +
          "[RSA 4096] Duration: " +
          colorama.Fore.BLUE +
          str(end -
              start) +
          colorama.Fore.RESET)
    print(
        colorama.Fore.YELLOW +
        "[RSA 4096] CPU Usage: " +
        colorama.Fore.CYAN +
        f"{end_cpu_usage:.2f}%" +
        colorama.Fore.RESET)

    return end - start


# Test each algorithm in a single-threaded environment.
def single_thread_test():
    print("Single-threaded test:")
    test_aes()
    test_blowfish()
    test_sha256()
    test_sha384()
    test_sha512()
    test_hmac()
    rsa_varied_key_size_st()


# Test each algorithm in a multi-threaded environment.
def multi_thread_test():
    print("Multi-threaded test:")
    threads = [
        threading.Thread(
            target=test_aes), threading.Thread(
            target=test_blowfish), threading.Thread(
                target=test_sha256), threading.Thread(
                    target=test_sha384), threading.Thread(
                        target=test_sha512), threading.Thread(
                            target=test_hmac), threading.Thread(
                                target=rsa_varied_key_size_mt)]

    for thread in threads:
        thread.start()

    for thread in threads:
        thread.join()


if __name__ == "__main__":
    single_thread_test()
    multi_thread_test()

# Conclusion: RSA-2048 with multi-threading is the optimal choice for this application.
# Encrypt with AES, sign with RSA.
