import time
from unittest import TestCase
import sys
from unittest.mock import Mock
from Sensor.RangeSensor import RangeSensor

sys.path.append('./')

from SumpOverflowAlert import config
from SumpOverflowAlert.App import App


__author__ = 'John Sonneville'


class TestApp(TestCase):
    def __init__(self, method_name='runTest'):
        super().__init__(method_name)

    def setUp(self):
        self.current_distance = config.trigger_distance
        self.max_loops = 1
        config.alert_after = 1
        self.loop_count = 0
        self.sensor_mock = Mock()
        self.sensor_mock.get_distance.side_effect = self.getDistanceStub
        self.last_duration = 0
        self.start_time = self.get_milliseconds()
        self.app = App(self.sensor_mock)

    def get_milliseconds(self):
        return time.time() * 1000

    def get_elapsed_milliseconds(self):
        return round(self.get_milliseconds() - self.start_time, 0)

    def shouldContinue(self):
        return self.get_elapsed_milliseconds() < (config.alert_after * 1000) or self.loop_count < self.max_loops - 1

    def getDistanceStub(self):
        if self.loop_count >= 1:
            self.last_duration = round(self.get_milliseconds() - self.last_called_time, 0)
        self.last_called_time = self.get_milliseconds()
        self.app.shouldContinue = self.shouldContinue()
        self.loop_count += 1
        return self.current_distance

    def test_creates_notifier(self):
        self.assertEqual(self.app.notifier.username, config.gmail['username'])
        self.assertEqual(self.app.notifier.password, config.gmail['password'])

    def test_creates_range_sensor(self):
        self.assertIsNotNone(self.app.rangeSensor)

    def test_should_use_default_RangeSensor(self):
        app = App()

        self.assertTrue(isinstance(app.rangeSensor, RangeSensor.__class__))

    def test_should_sleep_100_between_measurements(self):
        self.app.run()

        self.assertEqual(self.last_duration, 100)

    def test_should_sleep_10_when_less_than_trigger_distance(self):
        self.current_distance = 9

        self.app.run()

        self.assertEqual(self.last_duration, 10)

    def test_should_send_alert_if_over_threshold(self):
        self.app.run()

        self.assertEqual(self.get_elapsed_milliseconds() // 1000, config.alert_after)