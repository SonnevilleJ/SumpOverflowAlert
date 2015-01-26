import smtplib


class GmailNotifier(object):
    def __init__(self, username, password):
        super().__init__()
        self.username = username
        self.password = password

    def __send_email(self, message):
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.ehlo()
        server.starttls()
        server.login(self.username, self.password)
        server.sendmail(self.username, [self.username], message)
        server.close()

    def __format_email(self, subject):
        return """From: %s\nTo: %s\nSubject: %s\n\n%s""" % \
               (self.username, ", ".join([self.username]), subject, "")

    def send_notification(self):
        subject = "Sump Overflow Notification"
        message = self.__format_email(subject)
        self.__send_email(message)

    def send_all_clear(self):
        subject = "Sump Level Normal"
        message = self.__format_email(subject)
        self.__send_email(message)
