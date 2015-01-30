import sys
from unittest import mock
from unittest import TestCase

from Sleeper.sleeper import Sleeper

sys.path.append('./')


class TestSleeper(TestCase):
    def setUp(self):
        self.sleeper = Sleeper()

    @mock.patch("SumpOverflowAlert.Sleeper.sleeper.time.sleep")
    def test_sleep(self, mock_sleep):
        self.sleeper.sleep(10)

        mock_sleep.assert_called_with(10)