#! /usr/bin/env python

from APDUCommunicator import APDUCommunicator


def run():
    com = APDUCommunicator()
    com.request_otp()


if __name__ == "__main__":
    while True:
        run()
