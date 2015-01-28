from unittest import TestCase
import sys
sys.path.append('../')

from SumpOverflowAlert import config
from SumpOverflowAlert.App import App


__author__ = 'John Sonneville'


class TestApp(TestCase):
    def __init__(self, method_name='runTest'):
        super().__init__(method_name)

    def setUp(self):
        self.app = App()

    def test_creates_notifier(self):
        self.assertEqual(self.app.notifier.username, config.gmail['username'])
        self.assertEqual(self.app.notifier.password, config.gmail['password'])

    def test_creates_range_sensor(self):
        self.assertIsNotNone(self.app.rangeSensor)