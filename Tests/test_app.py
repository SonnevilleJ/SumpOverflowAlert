import time
from unittest import TestCase
import sys
from unittest.mock import Mock

from Sensor import RangeSensor
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
        self.max_loops = 300
        config.alert_after = 1
        self.loop_count = 0
        self.sensor_mock = Mock()
        self.notifier_mock = Mock()
        self.sleeper_mock = Mock()
        self.app = App(self.sensor_mock, self.notifier_mock, self.sleeper_mock)

    def shouldContinue(self):
        return self.loop_count < self.max_loops

    def sendNotificationStub(self):
        self.sleeper_mock.sleep.assert_called_with(0.01)
        self.assertEqual(self.sleeper_mock.sleep.call_count, 100)

    def sendAllClearStub(self):
        self.sleeper_mock.sleep.assert_called_with(0.01)
        self.assertEqual(self.sleeper_mock.sleep.call_count, 101)

    def test_default_constructor_values(self):
        self.app = App()

        self.assertEqual(self.app.notifier.username, config.gmail['username'])
        self.assertEqual(self.app.notifier.password, config.gmail['password'])
        # self.assertTrue(isinstance(self.app.rangeSensor, RangeSensor.RangeSensor))
        # self.assertTrue(isinstance(self.app.sleeper, Sleeper))

    def test_creates_range_sensor(self):
        self.assertIsNotNone(self.app.rangeSensor)

    def test_should_sleep_100_between_measurements(self):
        def get_distance_stub():
            self.app.shouldContinue = self.shouldContinue()
            self.loop_count += 1
            return self.current_distance
        self.sensor_mock.get_distance.side_effect = get_distance_stub

        self.app.run()

        self.sleeper_mock.sleep.assert_called_with(0.1)

    def test_should_sleep_10_when_less_than_trigger_distance(self):
        def get_distance_stub():
            self.app.shouldContinue = self.shouldContinue()
            self.loop_count += 1
            return self.current_distance
        self.sensor_mock.get_distance.side_effect = get_distance_stub
        self.current_distance = 9
        self.notifier_mock.send_notification.side_effect = self.sendNotificationStub

        self.app.run()

        self.notifier_mock.send_notification.assert_called_with()

    def test_should_sleep_100_after_returning_past_trigger_distance(self):
        def get_distance_stub():
            if self.loop_count == 100:
                self.current_distance = config.trigger_distance
            self.app.shouldContinue = self.shouldContinue()
            self.loop_count += 1
            return self.current_distance
        self.sensor_mock.get_distance.side_effect = get_distance_stub
        self.notifier_mock.send_all_clear.side_effect = self.sendAllClearStub
        self.current_distance = 9

        self.app.run()

        self.notifier_mock.send_all_clear.assert_called_with()