from APDUCommunicator import APDUCommunicator
import Encryption
from APDUHeader import APDUHeader
from MessageConverter import MessageConverter

def basic_diffie():

    n = "23"
    g = "5"
    x = "6"

    com = APDUCommunicator()

    com.send_message(APDUHeader.SEND_DH_N, n)
    com.send_message(APDUHeader.SEND_DH_G, g)
    bob_sends = com.send_message(APDUHeader.SEND_DH_ALICE, str(Encryption.dh_alice_sends(int(n), int(g), int(x))))
    print ("Bob: " + MessageConverter.byte_array_to_string(bob_sends))



    aes_key = str(int(MessageConverter.byte_array_to_string(bob_sends)) ** int(x) % int(n)).encode()

    otp = com.send_message(APDUHeader.REQUEST_OTP_DH, "")
    otp = MessageConverter.byte_array_to_string(otp)
    print(otp)
    print (Encryption.aes_decrypt(otp, aes_key))


basic_diffie()

