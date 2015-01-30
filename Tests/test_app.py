import time
from unittest import TestCase
import sys
from unittest.mock import Mock

from Sensor.RangeSensor import RangeSensor
from sleeper import Sleeper


sys.path.append('./')

from SumpOverflowAlert import config
from SumpOverflowAlert.App import App


__author__ = 'John Sonneville'


class TestApp(TestCase):
    def __init__(self, method_name='runTest'):
        super().__init__(method_name)

    def setUp(self):
        self.current_distance = config.trigger_distance
        self.max_loops = 2
        config.alert_after = 1
        self.loop_count = 0
        self.sensor_mock = Mock()
        self.sensor_mock.get_distance.side_effect = self.getDistanceStub
        self.notifier_mock = Mock()
        self.sleeper_mock = Mock()
        self.app = App(self.sensor_mock, self.notifier_mock, self.sleeper_mock)

    def shouldContinue(self):
        return self.loop_count < self.max_loops

    def getDistanceStub(self):
        if self.loop_count >= 1:
            self.current_distance = config.trigger_distance
        self.app.shouldContinue = self.shouldContinue()
        self.loop_count += 1
        return self.current_distance

    def sendNotificationStub(self):
        pass

    def test_default_constructor_values(self):
        self.app = App()

        self.assertEqual(self.app.notifier.username, config.gmail['username'])
        self.assertEqual(self.app.notifier.password, config.gmail['password'])

    def test_creates_range_sensor(self):
        self.assertIsNotNone(self.app.rangeSensor)

    def test_should_sleep_100_between_measurements(self):
        self.app.run()

        self.sleeper_mock.sleep.assert_called_with(0.1)

    def test_should_sleep_10_when_less_than_trigger_distance(self):
        self.max_loops = 1
        self.current_distance = 9

        self.app.run()

        self.sleeper_mock.sleep.assert_called_with(0.01)

    def test_should_sleep_100_after_returning_past_trigger_distance(self):
        self.current_distance = 9

        self.app.run()

        self.sleeper_mock.sleep.assert_called_with(0.1)