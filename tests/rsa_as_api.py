import time

from fastapi import FastAPI, Request, HTTPException
from Cryptodome.Cipher import AES
from Cryptodome.Util.Padding import pad
import base64
import threading
import redis
import rsa
import random
import string
import psutil
import colorama
from redis import Redis
from starlette import status

app = FastAPI()
r: Redis = redis.Redis(host='localhost', port=6379)

# Global variables to store the keys
public_key = None
private_key = None
aes_secret = None
aes_iv = None


def create_keys():
    global public_key, private_key
    (public_key, private_key) = rsa.newkeys(
        2048, poolsize=int(psutil.cpu_count()) - 2)
    # Save the keys in Redis
    r.set('public_key', public_key.save_pkcs1())
    r.set('private_key', private_key.save_pkcs1())
    print(colorama.Fore.GREEN + "RSA Keys generated" + colorama.Fore.RESET)


def generate_aes_secret_and_iv():
    global aes_secret, aes_iv
    aes_secret = ''.join(
        random.choices(
            string.ascii_letters +
            string.digits,
            k=16)).encode()
    aes_iv = ''.join(
        random.choices(
            string.ascii_letters +
            string.digits,
            k=16)).encode()
    r.set('aes_secret', aes_secret)
    r.set('aes_iv', aes_iv)
    print(
        colorama.Fore.GREEN +
        "AES Secret and IV generated" +
        colorama.Fore.RESET)


# Start threads to generate keys and AES secret/IV
thread_rsa = threading.Thread(target=create_keys)
thread_aes = threading.Thread(target=generate_aes_secret_and_iv)

thread_rsa.start()
thread_aes.start()

thread_rsa.join()
thread_aes.join()


@app.get("/")
async def root():
    # Get some system information
    cpu_count = psutil.cpu_count()
    cpu_usage = psutil.cpu_percent()
    memory_usage = psutil.virtual_memory().percent
    disk_usage = psutil.disk_usage('/').percent
    return {
        'cpu_count': cpu_count,
        'cpu_usage': cpu_usage,
        'memory_usage': memory_usage,
        'disk_usage': disk_usage}


@app.post("/rsa")
async def rsa_as_api(request: Request):
    # Rate limit after 5 requests in 10 seconds
    if r.get(request.client.host) is None:
        r.set(request.client.host, 1, ex=10)
    else:
        if int(r.get(request.client.host)) >= 5:
            # Return a code 429 (Too Many Requests)
            raise HTTPException(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                detail=f'You have been rate limited.',
            )
        else:
            r.incr(request.client.host)

    # Get the request body
    try:
        body = await request.json()
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f'Invalid JSON provided.',
        )
    if not body['message']:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f'No message provided.',
        )
    global aes_secret, aes_iv

    # Pad the message if it's not a multiple of 16
    if len(body['message']) % 16 != 0:
        body['message'] = pad(body['message'].encode(), 16)

    start = time.time()

    # Encrypt the message with AES
    cipher = AES.new(aes_secret, AES.MODE_CBC, aes_iv)
    encrypted_message = cipher.encrypt(body['message'])

    # Get the private key from Redis
    private_key = rsa.PrivateKey.load_pkcs1(r.get('private_key'))

    # Sign the message with RSA
    signature = rsa.sign(encrypted_message, private_key, 'SHA-256')

    # Encode the encrypted message and signature in base64
    encrypted_message = base64.b64encode(encrypted_message).decode()
    signature = base64.b64encode(signature).decode()

    end = time.time()

    time_taken = round(end - start, 2)
    time_taken = str(
        time_taken) + "s" if time_taken > 1 else str(round(time_taken * 1000, 2)) + "ms"

    # Return the encrypted message and signature
    return {
        'encrypted_message': encrypted_message,
        'signature': signature,
        'time_taken': time_taken}
