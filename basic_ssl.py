from APDUCommunicator import APDUCommunicator
from APDUHeader import APDUHeader
from Encryption import generate_aes_key
from MessageConverter import MessageConverter
from base64 import b64decode,b64encode
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_v1_5 as Cipher_PKCS1_v1_5
from binascii import hexlify
import base64

com = APDUCommunicator()
public_key = MessageConverter.byte_array_to_string(com.send_message(APDUHeader.REQUEST_PUBLIC_KEY, ""))

aes_key = generate_aes_key()

keyDER = b64decode(public_key)
keyPub = RSA.importKey(keyDER)

cipher = Cipher_PKCS1_v1_5.new(keyPub)
cipher_text = cipher.encrypt("hello".encode())
b64message = base64.b64encode(cipher_text)
print(cipher_text.hex())
print(b64message)

print(MessageConverter.format_hex_array(b64message.hex()))

com.send_preencoded_message(APDUHeader.SEND_AES_KEY, MessageConverter.format_hex_array(b64message.hex()))


