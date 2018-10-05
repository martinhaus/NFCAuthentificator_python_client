#! /usr/bin/env python

from smartcard.System import readers
from smartcard.util import toHexString

basic_apdu = [0x00, 0xA4, 0x04, 0x00]
end_apdu = [0x00]


APDU = [0x00, 0xA4, 0x04, 0x00, 0x05, 0xF2, 0x22, 0x22, 0x22, 0x22, 0x00]
APDU2 = [0x00, 0xA4, 0x04, 0x00, 0x02,0x11,  0x00]
# get all the available readers
r = readers()
reader = r[0]
print ("Using:", reader)

connection = reader.createConnection()
connection.connect()

data, sw1, sw2 = connection.transmit(APDU)
print (toHexString(data))
print ("Command: %02X %02X" % (sw1, sw2))


data, sw1, sw2 = connection.transmit(APDU2)
print (toHexString(data))
print ("Command: %02X %02X" % (sw1, sw2))


