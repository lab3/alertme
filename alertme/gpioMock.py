import time


class gpioMock:
    def __init__(self, zones, action):
        print("gpioMock Init")
        self.pins = list(zones.keys())
        self.action = action
        self.zones = zones

    def run(self):
        count = 1
        while True:
            for pin in self.pins:
                zone = self.zones[pin]
                if(count % 10 == 0):
                    print("mock set pin true:" + str(pin))
                    self.action(pin, True)
                elif(count % 51 == 0):
                    print("mock set pin false:" + str(pin))
                    self.action(pin, False)
            time.sleep(0.5)
            count += 1
