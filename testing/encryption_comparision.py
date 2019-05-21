from android_nfc_com.APDUCommunicator import APDUCommunicator
import time
import statistics

class APDUTimeTesting:

    def __init__(self):
        pass

    @staticmethod
    def asymmetric(count, always_new_instance=False):
        results = []
        start = time.time()
        a = APDUCommunicator('asymmetric', False)
        for i in range(count):

            if always_new_instance:
                single_start = time.time()
                del a
            a = APDUCommunicator('asymmetric', False)
            a.request_otp()
            single_stop = time.time()
            results.append(single_stop - single_start)
            print(str(i) + "/" + str(count) + " " + str(single_stop - single_start))

        # end = time.time()

        print("STDEV: " + str(statistics.stdev(results)))
        print("MEDIAN: " + str(statistics.median(results)))
        print("MEAN: " + str(statistics.mean(results)))

        # return (end - start) / count


    @staticmethod
    def diffie_hellman(count, always_new_instance=False):
        results = []

        # start = time.time()
        a = APDUCommunicator('diffie-hellman', False)
        for i in range(count):
            # time.sleep(0.2)
            if always_new_instance:
                del a
                single_start = time.time()
                a = APDUCommunicator('diffie-hellman', False)

            a.request_otp()
            single_stop = time.time()
            results.append(single_stop - single_start)
            print(str(i) + "/" + str(count) + " " + str(single_stop - single_start))

        # end = time.time()
        print("STDEV: " + str(statistics.stdev(results)))
        print("MEDIAN: " + str(statistics.median(results)))
        print("MEAN: " + str(statistics.mean(results)))

        return sum (results) / count


if __name__ == "__main__":

    # print('ASSYMETRIC 1000 ', APDUTimeTesting.diffie_hellman(100, True))
    print('DH 1000 ', APDUTimeTesting.asymmetric(100, True))


