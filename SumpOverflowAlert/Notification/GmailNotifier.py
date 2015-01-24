import smtplib

__author__ = 'John Sonneville'


class GmailNotifier(object):
    def __init__(self):
        super().__init__()

    def send_notification(self):
        server = smtplib.SMTP('smtp.gmail.com', 587)

        server.close()