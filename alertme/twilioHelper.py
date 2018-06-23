import datetime
import traceback
from twilio.rest import TwilioRestClient


class twilioHelper:
    def __init__(self, sid, token):
        self.ACCOUNT_SID = sid
        self.AUTH_TOKEN = token
        self.client = TwilioRestClient(self.ACCOUNT_SID, self.AUTH_TOKEN)

    def sendMessage(self, message, from_, to):
        print(str(datetime.datetime.now()) + " send " + from_ + " -> " + to + " " + message)

        try:
            self.client.messages.create(
                to=to,
                from_=from_,
                body=message)
            return True
        except:
            print(traceback.print_exc())
            return False


class twilioHelperMock:
    def __init__(self, sid, token):
        print("twilioHelperMock Init")

    def sendMessage(self, message, from_, to):
        try:
            print(str(datetime.datetime.now()) + " send " + from_ + " -> " + to + " " + message)
            return True
        except:
            print(str(datetime.datetime.now()) + "send failed")
            print(traceback.print_exc())
            return False
