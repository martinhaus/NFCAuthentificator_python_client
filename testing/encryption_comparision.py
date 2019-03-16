from android_nfc_com.APDUCommunicator import APDUCommunicator
import time


class APDUTimeTesting:

    def __init__(self):
        pass

    @staticmethod
    def asymmetric(count, always_new_instance=True):

        start = time.time()
        a = APDUCommunicator('asymmetric', False)
        for i in range(count):
            # if always_new_instance:
            del a
            a = APDUCommunicator('asymmetric', False)
            a.request_otp()

        end = time.time()

        return (end - start) / count


    @staticmethod
    def diffie_hellman(count, always_new_instance=False):

        start = time.time()
        a = APDUCommunicator('diffie-hellman', False)
        for i in range(count):
            if always_new_instance:
                del a
                a = APDUCommunicator('diffie-hellman', False)
            a.request_otp()

        end = time.time()

        return (end - start) / count


if __name__ == "__main__":

    print('ASSYMETRIC 1000 ', APDUTimeTesting.asymmetric(1, False))
    # print('DH 1000 ', APDUTimeTesting.diffie_hellman(10, True))


