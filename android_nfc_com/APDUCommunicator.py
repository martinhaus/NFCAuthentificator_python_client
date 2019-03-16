import base64
import json
import random
from base64 import b64decode

from Crypto.PublicKey import RSA
from smartcard.System import readers
from smartcard.util import toHexString
from Crypto.Cipher import PKCS1_v1_5 as Cipher_PKCS1_v1_5
from android_nfc_com import Encryption, config
from android_nfc_com.APDUMessage import APDUMessage
from android_nfc_com.APDUHeader import APDUHeader
from android_nfc_com.APDUMessageConverter import MessageConverter
from smartcard.CardRequest import CardRequest
import logging


class APDUCommunicator:

    def __init__(self, method=None, waiting=True):
        self.connection = self.__send_intro_message(waiting)
        self.aes_key = None
        self.exchange_key(method)

    def send_message(self, header, body):
        """ send introduction message and follow with all messages """

        # If body is string convert it to byte array
        if isinstance(body, str):
            body = MessageConverter.string_to_byte_array(body)

        message = APDUMessage(header, body).convertToByteArray()
        data, sw1, sw2 = self.connection.transmit(message)

        logging.debug('Sending message: ', message)
        logging.debug('Got response: ', toHexString(data))
        logging.debug('Got status code:  %02X %02X' % (sw1, sw2))

        # If message is encrypted, decrypt it
        if self.aes_key is not None:
            data = Encryption.aes_decrypt(MessageConverter.byte_array_to_string(data), self.aes_key)

        return data

    def __send_intro_message(self, waiting):
        """ sends introduction message and returns active connection to device """

        logging.debug('Initialized communication. waiting for device...')

        if waiting:
            cardrequest = CardRequest(timeout=3000)
            cardrequest.waitforcard()

        r = readers()
        reader = r[0]

        connection = reader.createConnection()
        connection.connect()

        logging.debug('Connected to device. ')
        logging.debug('Sending initial message with AID.')

        # Send introductory message with AID from configuration file
        intro_message = APDUMessage(APDUHeader.SELECT_AID, config.AID).convertToByteArray()

        data, sw1, sw2 = connection.transmit(intro_message)

        logging.debug('Got response: %02X %02X' % (sw1, sw2))

        # Return active connection that is later used to communicate with device
        return connection

    def __diffie_hellman_exchange(self):
        """ Exchange AES key with Android device using Diffie-Hellman key exchange method """

        # Load pre-generated primes from file
        with open('../primes.json', 'r') as input_primes:
            primes = json.load(input_primes)

        # Randomly choose one pair of prime and it's primitive root modulo
        random_pair = random.choice(primes)

        n = random_pair['prime']
        g = random_pair['root']

        # Randomly choose alice secret
        x = random.getrandbits(5)

        # Send prime and primitive root modulo (both publicly known, we are sending over insecure channel) to device

        self.send_message(APDUHeader.SEND_DH_N, str(n))
        self.send_message(APDUHeader.SEND_DH_G, str(g))
        # Send our calculated value to the device and request their calculated value at the same time
        bob_sends = self.send_message(APDUHeader.SEND_DH_ALICE, str((g ** x) % n))

        # Construct key later to be used in AES cipher
        aes_key = str(int(MessageConverter.byte_array_to_string(bob_sends)) ** x % n).encode()
        self.aes_key = aes_key

    def __asymmetric_key_exchange(self):
        """ Exchange AES key with Android device using asymmetric key exchange method """

        # Request public key from device
        public_key = MessageConverter.byte_array_to_string(self.send_message(APDUHeader.REQUEST_PUBLIC_KEY, ""))

        # Generate AES key for later encryption
        aes_key = Encryption.generate_aes_key().encode()

        # Decode public key received from Android device
        keyDER = b64decode(public_key)
        keyPub = RSA.importKey(keyDER)

        # Encrypt AES key and send it to device
        cipher = Cipher_PKCS1_v1_5.new(keyPub)
        cipher_text = cipher.encrypt(aes_key)
        b64message = base64.b64encode(cipher_text)
        self.send_message(APDUHeader.SEND_AES_KEY, MessageConverter.format_hex_array(b64message.hex()))

        self.aes_key = aes_key

    def exchange_key(self, method=None):

        if method is None:
            method = config.key_transfer_method

        if method == 'asymmetric':
            self.__asymmetric_key_exchange()
        elif method == 'diffie-hellman':
            self.__diffie_hellman_exchange()
        else:
            self.__asymmetric_key_exchange()

    def request_otp(self):
        """ Request one time password from device """

        otp = self.send_message(APDUHeader.REQUEST_OTP, "")
        # self.connection.disconnect()
        # print(otp)

        return otp

