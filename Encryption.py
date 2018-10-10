import base64
import hashlib
from random import randint, randrange
from secrets import token_bytes

from Crypto.Cipher import AES
from Crypto.PublicKey import RSA
from Crypto.Util.Padding import unpad

from MessageConverter import MessageConverter


def diffiehelman(secret):
    # n = generatePrime(1024)  # publicly known
    # g = generatePrime(1024)  # publicly known

    n = 23
    g = 5

    x = 6  # only Alice knows this
    y = 15  # only Bob knows this

    aliceSends = (g ** x) % n
    bobComputes = aliceSends ** y % n
    bobSends = (g ** y) % n
    aliceComputes = bobSends ** x % n

    print ("Alice sends    ", aliceSends)
    print ("Bob computes   ", bobComputes)
    print ("Bob sends      ", bobSends)
    print ("Alice computes ", aliceComputes)

    print ("In theory both should have ", (g ** (x * y)) % n)

def dh_alice_sends(n ,g ,x):
    return (g ** x) % n


def generatePrime(size):
    return RSA.generate(size * 2).p

###################################################


def generate_aes_key():
    """ generate 128 bit AES key """
    return token_bytes(16)


def aes_decrypt(encrypted, key):
    key = hashlib.sha256(key).digest()
    encrypted = base64.b64decode(encrypted)
    # iv = encrypted[:AES.block_size]
    # iv = bytes([0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00])
    # print(iv)
    cipher = AES.new(key, AES.MODE_ECB)
    print(cipher.decrypt(encrypted))
    return unpad(cipher.decrypt(encrypted), AES.block_size).decode('utf-8')

