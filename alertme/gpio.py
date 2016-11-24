import RPi.GPIO as io
import time


class gpio:
    def __init__(self, zones, action):
        io.setmode(io.BCM)
        self.pins = list(zones.keys())

        for pin in self.pins:
            io.setup(pin, io.IN, pull_up_down=io.PUD_UP)
            #print("pin init:" + str(pin))

        self.action = action
        #print("io.LOW:" + str(io.LOW))
        #print("io.HIGH:" + str(io.HIGH))

    def run(self):
        while True:
            for pin in self.pins:
                #print(str(pin))
                self.action(pin, io.input(pin))
            time.sleep(0.5)
