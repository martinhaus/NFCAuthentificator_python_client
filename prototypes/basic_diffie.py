from android_nfc_com.APDUCommunicator import APDUCommunicator
from android_nfc_com import Encryption
from android_nfc_com.APDUHeader import APDUHeader
from android_nfc_com.APDUMessageConverter import MessageConverter
import json
import random


def basic_diffie():

    # Load pre-generated primes from file
    with open('primes.json', 'r') as input_primes:
        primes = json.load(input_primes)

    # Randomly choose one pair of prime and it's primitive root modulo
    random_pair = random.choice(primes)

    n = random_pair['prime']
    g = random_pair['root']

    x = 6

    com = APDUCommunicator()

    com.send_message(APDUHeader.SEND_DH_N, str(n))
    com.send_message(APDUHeader.SEND_DH_G, str(g))
    bob_sends = com.send_message(APDUHeader.SEND_DH_ALICE, str(Encryption.dh_alice_sends(n, g, x)))
    print ("Bob: " + MessageConverter.byte_array_to_string(bob_sends))

    aes_key = str(int(MessageConverter.byte_array_to_string(bob_sends)) ** x % n).encode()

    otp = com.send_message(APDUHeader.REQUEST_OTP_DH, "")
    otp = MessageConverter.byte_array_to_string(otp)
    print(otp)
    print (Encryption.aes_decrypt(otp, aes_key))


