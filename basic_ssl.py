import base64
from base64 import b64decode

from Crypto.Cipher import PKCS1_v1_5 as Cipher_PKCS1_v1_5
from Crypto.PublicKey import RSA

from APDUCommunicator import APDUCommunicator
from APDUHeader import APDUHeader
from Encryption import generate_aes_key
from MessageConverter import MessageConverter
from Encryption import aes_decrypt
com = APDUCommunicator()
public_key = MessageConverter.byte_array_to_string(com.send_message(APDUHeader.REQUEST_PUBLIC_KEY, ""))

aes_key = generate_aes_key()
aes_key = 'sdgiugtgfhdkfjnghfkdnghlfdghklnfkghjnfdgnhjlkdfghjoidgfifgdbiof41422bi'.encode()
keyDER = b64decode(public_key)
keyPub = RSA.importKey(keyDER)

cipher = Cipher_PKCS1_v1_5.new(keyPub)
cipher_text = cipher.encrypt(aes_key)
b64message = base64.b64encode(cipher_text)
com.send_preencoded_message(APDUHeader.SEND_AES_KEY, MessageConverter.format_hex_array(b64message.hex()))

otp = com.send_message(APDUHeader.REQUEST_OTP, "")
otp = MessageConverter.byte_array_to_string(otp)
print(otp)
print (aes_decrypt(otp, aes_key))




