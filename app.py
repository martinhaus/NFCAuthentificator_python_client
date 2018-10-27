#! /usr/bin/env python
from time import sleep

from smartcard.CardMonitoring import CardObserver, CardMonitor

from APDUCommunicator import APDUCommunicator


class PhoneObserver(CardObserver):

    def update(self, observable, actions):
        (addedcards, removedcards) = actions
        for card in addedcards:
            com = APDUCommunicator()
            com.request_otp()


def run():
    cardmonitor = CardMonitor()
    cardobserver = PhoneObserver()
    cardmonitor.addObserver(cardobserver)

    sleep(10)

    cardmonitor.deleteObserver(cardobserver)



if __name__ == "__main__":
    while True:
        run()
