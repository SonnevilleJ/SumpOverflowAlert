from unittest import mock
from unittest import TestCase

from SumpOverflowAlert.Notification import GmailNotifier


class TestGmailNotifier(TestCase):
    def setUp(self):
        self.username = "username"
        self.password = "password"
        self.notifier = GmailNotifier.GmailNotifier(self.username, self.password)

    def __verify_sent_email(self, mock_smtplib, subject):
        mock_smtplib.SMTP.assert_called_with('smtp.gmail.com', 587)
        mock_server = mock_smtplib.SMTP.return_value
        mock_server.ehlo.assert_called_with()
        mock_server.starttls.assert_called_with()
        mock_server.login.assert_called_with(self.username, self.password)
        message = """From: %s\nTo: %s\nSubject: %s\n\n%s""" % \
                  (self.username, ", ".join([self.username]), subject, "")
        print("Expected message follows:")
        print(message)
        mock_server.sendmail.assert_called_with(self.username, [self.username], message)
        mock_server.close.assert_called_with()

    @mock.patch("SumpOverflowAlert.Notification.GmailNotifier.smtplib")
    def test_send_notification(self, mock_smtplib):
        self.notifier.send_notification()

        subject = "Sump Overflow Notification"
        self.__verify_sent_email(mock_smtplib, subject)

    @mock.patch("SumpOverflowAlert.Notification.GmailNotifier.smtplib")
    def test_send_all_clear(self, mock_smtplib):
        self.notifier.send_all_clear()

        subject = "Sump Level Normal"
        self.__verify_sent_email(mock_smtplib, subject)
