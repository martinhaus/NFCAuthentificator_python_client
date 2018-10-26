import base64
import json
import random
from base64 import b64decode
from Crypto.Cipher import PKCS1_v1_5 as Cipher_PKCS1_v1_5
from Crypto.PublicKey import RSA
import Encryption
from APDUCommunicator import APDUCommunicator
from APDUHeader import APDUHeader
from MessageConverter import MessageConverter
import config


class APDUKeyExchange:

    @staticmethod
    def diffie_hellman_exchange():
        """ Exchange AES key with Android device using Diffie-Hellman key exchange method """

        # Load pre-generated primes from file
        with open('primes.json', 'r') as input_primes:
            primes = json.load(input_primes)

        # Randomly choose one pair of prime and it's primitive root modulo
        random_pair = random.choice(primes)

        n = random_pair['prime']
        g = random_pair['root']

        # Randomly choose alice secret
        x = random.randint(1, 10**12)

        # Send prime and primitive root modulo (both publicly known, we are sending over insecure channel) to device
        com = APDUCommunicator()

        com.send_message(APDUHeader.SEND_DH_N, str(n))
        com.send_message(APDUHeader.SEND_DH_G, str(g))

        # Send our calculated value to the device and request their calculated value at the same time
        bob_sends = com.send_message(APDUHeader.SEND_DH_ALICE, str((g ** x) % n))

        # Construct key later to be used in AES cipher
        aes_key = str(int(MessageConverter.byte_array_to_string(bob_sends)) ** x % n).encode()

        # otp = com.send_message(APDUHeader.REQUEST_OTP_DH, "")
        # otp = MessageConverter.byte_array_to_string(otp)
        # print(otp)
        # print(Encryption.aes_decrypt(otp, aes_key))

        return aes_key

    @staticmethod
    def asymmetric_key_exchange():
        """ Exchange AES key with Android device using asymmetric key exchange method """

        # Request public key from device
        com = APDUCommunicator()
        public_key = MessageConverter.byte_array_to_string(com.send_message(APDUHeader.REQUEST_PUBLIC_KEY, ""))

        # Generate AES key for later encryption
        aes_key = Encryption.generate_aes_key().encode()

        # Decode public key received from Android device
        keyDER = b64decode(public_key)
        keyPub = RSA.importKey(keyDER)

        # Encrypt AES key and send it to device
        cipher = Cipher_PKCS1_v1_5.new(keyPub)
        cipher_text = cipher.encrypt(aes_key)
        b64message = base64.b64encode(cipher_text)
        com.send_message(APDUHeader.SEND_AES_KEY, MessageConverter.format_hex_array(b64message.hex()))

        return aes_key

        # otp = com.send_message(APDUHeader.REQUEST_OTP, "")
        # otp = MessageConverter.byte_array_to_string(otp)
        # print('KEY: ', aes_decrypt(otp, aes_key))

    @staticmethod
    def exchange_key():
        if config.key_transfer_method == 'asymmetric':
            APDUKeyExchange.asymmetric_key_exchange()
        elif config.key_transfer_method == 'diffie-hellman':
            APDUKeyExchange.asymmetric_key_exchange()
        else:
            APDUKeyExchange.asymmetric_key_exchange()
