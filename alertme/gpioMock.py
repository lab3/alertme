import time


class gpioMock:
    def __init__(self, pins, action):
        print("alertIOMock Init")
        self.pins = pins
        self.action = action

    def run(self):
        count = 1
        while True:
            for pin in self.pins:
                if(count % 10 == 0):
                    self.action(pin, True)
                else:
                    self.action(pin, False)
            time.sleep(0.5)
            count += 1
