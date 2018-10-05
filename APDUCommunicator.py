#! /usr/bin/env python

from smartcard.System import readers
from smartcard.util import toHexString
from APDUMessage import APDUMessage
from APDUHeader import APDUHeader
from MessageConverter import MessageConverter
from Encryption import generatePrime


class APDUCommunicator:

    def __init__(self):
        self.AID = [0xF2, 0x22, 0x22, 0x22, 0x22]
        self.connection = self.send_intro_message()

    def send_message(self, header, body):
        """ send introduction message and follow with all messages """

        message = APDUMessage(header, MessageConverter.string_to_byte_array(body)).convertToByteArray()
        data, sw1, sw2 = self.connection.transmit(message)
        print(toHexString(data))
        print("Command: %02X %02X" % (sw1, sw2))

        return data

    def send_preencoded_message(self, header, body):
        message = APDUMessage(header, body).convertToByteArray()
        data, sw1, sw2 = self.connection.transmit(message)
        print(toHexString(data))
        print("Command: %02X %02X" % (sw1, sw2))

        return data

    def send_intro_message(self):
        """ sends introduction message and returns active connection to device """
        r = readers()
        reader = r[0]

        connection = reader.createConnection()
        connection.connect()

        intro_message = APDUMessage(APDUHeader.SELECT_AID, self.AID).convertToByteArray()

        data, sw1, sw2 = connection.transmit(intro_message)
        print(toHexString(data))
        print("Command: %02X %02X" % (sw1, sw2))

        return connection

# sample_message = MessageConverter.string_to_byte_array("MIICIjANBgkqhkiG9w0BAQEFAAOCAg8AMIICCgKCAgEAjl2XH4XEihCmSz/EHK+SiEE+V0sz5HDU0cw9aI8T1aHAiLSFrHwEdksoY98b3daXRrRzPloeGV2p3uLQfefEqPMEnPjD0YAOO80CQ14HjSjsEB8qu3nAeYrWpN56CaqoMu2Ugi0SPGfcvwRIaVO5rockTT216PAUpfeVbex8x9FOV5ymYg31duX2cExbj33SaB4fi65l/qxJUr+8rwK5z8Spee0cee/Epza1ICUpF/AWKtqB3AvrFxKPgQBZA/0wkstLQi44NgN89o9cZZ3FXJ+FcouXwZWWjXBaef7V5rR/JtymoAAVYZq8jFINZI2pWswXD0qiFCC6yQpv7W464274qLNfkcYd47BQYAdeFjsf5XnJOjzNmDoYom9UTHFXwj6Sb6Ka1/CGqHVSXLkUbxsLZG1hqa4xHvedKmHMAk3nPNdfgikkyQ7aEEQEXo0vERvLxy33vVd5bbQT8bVeqzjSzU2FZRixVylMZ0If9PNYR2YninQndETF4o2CMXz3kY6A9g1Wl5HP7JNQ/kxS6zGh7HwJvuh242vxd6XDNy8E6VVkps9c0YQlmza6dvjp8HtNcBLel4uMT4WT8kF5POka6iG1XgAlU6dXWkhyRNUQEvrSf1xghchfJrZbJ07bO2R4mc5OgH7I2vxSlsGSyE0VOPbyAe5LrtQN2YQzf9ECAwEAAQ==")
# print(sample_message)



# following_message = APDUMessage(APDUHeader.SEND_DH_P, sample_message).convertToByteArray()
#
# dh_p_message = APDUMessage(APDUHeader.SEND_DH_P, MessageConverter.string_to_byte_array(str(generatePrime(1024)))).convertToByteArray()
# dh_q_message = APDUMessage(APDUHeader.SEND_DH_Q, MessageConverter.string_to_byte_array(str(2))).convertToByteArray()

# data, sw1, sw2 = connection.transmit(dh_q_message)
# print (toHexString(data))
# print ("Command: %02X %02X" % (sw1, sw2))

