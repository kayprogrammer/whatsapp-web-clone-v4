from setup.extensions import mail
from setup.settings import client
import threading

class EmailMessageThread(threading.Thread):

    def __init__(self, app, msg):
        self.msg = msg
        self.app = app
        threading.Thread.__init__(self)

    def run(self):
        with self.app.app_context():
            mail.send(self.msg)

class SmsMessageThread(threading.Thread):

    def __init__(self, body, from_, to):
        self.body = body
        self.from_ = from_
        self.to = to
        threading.Thread.__init__(self)

    def run(self):
        client.messages.create(
            body = self.body,
            from_ = self.from_,
            to = self.to
        )
