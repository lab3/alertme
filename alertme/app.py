#!/usr/bin/env python

# Testing
#from gpioMock import gpioMock as gpio
#from twilioHelper import twilioHelperMock as twilioHelper

# Live
from twilioHelper import twilioHelper
from gpio import gpio
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

    def handleRead(self, pin, isOpen):
        #print("handleRead: " + str(pin) + " " + str(isOpen))
        zone = self.zones[pin]
        #print("zone:" + str(zone.isOpen))

        if zone is not None:
            if(isOpen and not zone.isOpen):
                self.sendMessage(zone.name + " opened")
                zone.isOpen = True
            elif(not isOpen and zone.isOpen):
                zone.isOpen = False

    def sendMessage(self, message):
        timenow = datetime.datetime.now().time()

        if(timenow > self.on or timenow < self.off):
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
