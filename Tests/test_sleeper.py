import sys
from unittest import mock
from unittest import TestCase

from SumpOverflowAlert.sleeper import Sleeper


sys.path.append('./')


class TestSleeper(TestCase):
    def setUp(self):
        self.sleeper = Sleeper()

    @mock.patch("SumpOverflowAlert.sleeper.time.sleep")
    def test_sleep_10(self, mock_sleep):
        self.sleeper.sleep(10)

        mock_sleep.assert_called_with(10)

    @mock.patch("SumpOverflowAlert.sleeper.time.sleep")
    def test_sleep_20(self, mock_sleep):
        self.sleeper.sleep(20)

        mock_sleep.assert_called_with(20)