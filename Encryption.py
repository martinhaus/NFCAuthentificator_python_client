from random import randint, randrange
from secrets import token_bytes

from Crypto.PublicKey import RSA


def diffiehelman(secret):
    n = 22  # publicly known
    g = 42  # publicly known

    x = 13  # only Alice knows this
    y = 53  # only Bob knows this

    aliceSends = (g ** x) % n
    bobComputes = aliceSends ** y % n
    bobSends = (g ** y) % n
    aliceComputes = bobSends ** x % n

    print ("Alice sends    ", aliceSends)
    print ("Bob computes   ", bobComputes)
    print ("Bob sends      ", bobSends)
    print ("Alice computes ", aliceComputes)

    print ("In theory both should have ", (g ** (x * y)) % n)


def generatePrime(size):
    return RSA.generate(size * 2).p

###################################################


def generate_aes_key():
    """ generate 256 bit AES key """
    return token_bytes(32)

