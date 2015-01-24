from unittest import mock
from unittest import TestCase

from SumpOverflowAlert.Notification import GmailNotifier


__author__ = 'John Sonneville'


class GmailNotifierTest(TestCase):
    def setUp(self):
        self.notifier = GmailNotifier.GmailNotifier()

    @mock.patch("SumpOverflowAlert.Notification.GmailNotifier.smtplib")
    def test_opens_correct_address(self, mock_smtplib):
        self.notifier.send_notification()

        mock_smtplib.SMTP.assert_called_with('smtp.gmail.com', 587)
        mock_smtplib.SMTP.return_value.close.assert_called_with()
