#! /usr/bin/env python

from smartcard.System import readers
from smartcard.util import toHexString
from APDUMessage import APDUMessage
from APDUHeader import APDUHeader
from MessageConverter import MessageConverter
from smartcard.CardRequest import CardRequest
import logging
import config


class APDUCommunicator:

    def __init__(self):
        self.connection = self.send_intro_message()

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

        return data

    def send_intro_message(self):
        """ sends introduction message and returns active connection to device """

        logging.debug('Initialized communication. waiting for device...')

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

