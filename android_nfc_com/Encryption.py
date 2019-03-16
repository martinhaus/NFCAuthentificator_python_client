import base64
import hashlib
import random
import secrets
import string

from Crypto.Cipher import AES
from Crypto.Util import number
from Crypto.Util.Padding import unpad


def generatePrime(size):
    # return RSA.generate(size * 2).p
    return number.getPrime(size)


def generate_random_number(bits):
    return random.getrandbits(bits)


def generate_aes_key():
    alphabet = string.ascii_letters + string.digits
    password = ''.join(secrets.choice(alphabet) for i in range(20))
    return password


def aes_decrypt(encrypted, key):
    key = hashlib.sha256(key).digest()
    encrypted = base64.b64decode(encrypted)
    # iv = encrypted[:AES.block_size]
    # iv = bytes([0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00])
    # print(iv)
    cipher = AES.new(key, AES.MODE_ECB)
    # print(cipher.decrypt(encrypted))
    return unpad(cipher.decrypt(encrypted), AES.block_size, style='pkcs7').decode('utf-8')

