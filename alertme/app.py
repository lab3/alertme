#!/usr/bin/env python

# Testing
from gpioMock import gpioMock as gpio
from twilioHelper import twilioHelperMock as twilioHelper

# Live
#from twilioHelper import twilioHelper
# from gpio import gpio
from zone import zone
import datetime
import configparser


class app:
    def __init__(self, config, zones):
        self.c = config["alertme"]
        self.zones = {z.pin: z for z in zones}
        self.on = datetime.time(int(self.c["on_hh"]), int(self.c["on_mm"]))
        self.off = datetime.time(int(self.c["off_hh"]), int(self.c["off_mm"]))
        self.sms = twilioHelper(self.c["twilio_sid"], self.c["twilio_token"])
        self.duration_seconds = int(self.c["duration_seconds"])
        self.lastSendResult = True

    def handleRead(self, pin, isOpen):
        # print("handleRead: " + str(pin) + " " + str(isOpen))
        timenow = datetime.datetime.now().time()
        if(timenow > self.on or timenow <= self.off):
            zone = self.zones[pin]
        else:
            zone = None
        # print("zone:" + str(zone.isOpen))

        if(not self.lastSendResult):
            self.sendMessage("failed sending message")
            self.lastSendResult = True

        if zone is not None:
            if(isOpen and not zone.isOpen):
                zone.when = datetime.datetime.now()
                zone.isOpen = True
                self.lastSendResult = self.sendMessage(zone.name + " opened")
            elif(isOpen and zone.isOpen):
                diff = (datetime.datetime.now() - zone.when).total_seconds()
                print("diff:" + str(diff))
                if(diff > self.duration_seconds and not zone.durationTrigger):
                    zone.durationTrigger = True
                    self.lastSendResult = self.sendMessage(zone.name + " was left open")
            elif(not isOpen and zone.isOpen):
                zone.durationTrigger = False
                zone.isOpen = False
                self.lastSendResult = self.sendMessage(zone.name + " was closed")

    def sendMessage(self, message):
        timenow = datetime.datetime.now().time()

        if(timenow > self.on or timenow <= self.off):
            self.sms.sendMessage(message, self.c["sms_from"], self.c["sms_to"])

    def run(self):
        aio = gpio(self.zones, self.handleRead)
        aio.run()


config = configparser.ConfigParser()
config.read_file(open('alertme.cfg'))

zones = [
    zone(17, "Back door"),
    zone(7, "Front door")
]

app(config, zones).run()
