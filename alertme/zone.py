import datetime


class zone:
    def __init__(self, pin, name, isOpen=False, durationTrigger=False, when=datetime.datetime.now()):
        self.pin = pin
        self.name = name
        self.isOpen = isOpen
        self.when = when
        self.durationTrigger = durationTrigger
