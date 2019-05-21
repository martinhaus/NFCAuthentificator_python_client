#! /usr/bin/env python
from time import sleep

from smartcard.CardMonitoring import CardObserver, CardMonitor

from android_nfc_com.APDUCommunicator import APDUCommunicator


class PhoneObserver(CardObserver):

    def update(self, observable, actions):
        (addedcards, removedcards) = actions
        for card in addedcards:
            try:
                com = APDUCommunicator('diffie-hellman', 1024, False)
                com.request_otp()

            except Exception:
                print("Connection could not be established, please try again...")

def run():
    cardmonitor = CardMonitor()
    cardobserver = PhoneObserver()
    cardmonitor.addObserver(cardobserver)

    sleep(10)

    cardmonitor.deleteObserver(cardobserver)



if __name__ == "__main__":
    while True:
        run()
