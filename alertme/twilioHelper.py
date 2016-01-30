from twilio.rest import TwilioRestClient


class twilioHelper:
    def __init__(self, sid, token):
        self.ACCOUNT_SID = sid
        self.AUTH_TOKEN = token
        self.client = TwilioRestClient(self.ACCOUNT_SID, self.AUTH_TOKEN)

    def sendMessage(self, message, from_, to):
        self.client.messages.create(
            to=to,
            from_=from_,
            body=message)


class twilioHelperMock:
    def __init__(self, sid, token):
        None

    def sendMessage(self, message, from_, to):
        print("send:" + from_ + " -> " + to + " " + message)
