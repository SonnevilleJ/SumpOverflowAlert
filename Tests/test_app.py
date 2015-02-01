import sys

sys.path.append('./')

from unittest import TestCase
from unittest.mock import Mock
import mock

from SumpOverflowAlert import config
from SumpOverflowAlert.App import App


__author__ = 'John Sonneville'


class TestApp(TestCase):
    def __init__(self, method_name='runTest'):
        super().__init__(method_name)

    def setUp(self):
        self.current_distance = config.trigger_distance
        self.max_loops = 400
        config.alert_after = 1
        self.loop_count = 0
        self.sensor_mock = Mock()
        self.notifier_mock = Mock()
        self.app = App(self.sensor_mock, self.notifier_mock)

    def shouldContinue(self):
        return self.loop_count < self.max_loops

    def sendNotificationStub(self):
        print("called sendNotification on iteration: " + str(self.mock_time.sleep.call_count))
        self.mock_time.sleep.assert_called_with(0.01)
        count = (self.mock_time.sleep.call_count + 100) % 200
        self.assertEqual(0, count)

    def sendAllClearStub(self):
        print("called sendAllClear on iteration: " + str(self.mock_time.sleep.call_count))
        self.mock_time.sleep.assert_called_with(0.01)
        self.assertEqual(0, self.mock_time.sleep.call_count % 200)

    def test_default_constructor_values(self):
        self.app = App()

        self.assertEqual(self.app.notifier.username, config.gmail['username'])
        self.assertEqual(self.app.notifier.password, config.gmail['password'])
        # self.assertTrue(isinstance(self.app.rangeSensor, RangeSensor.RangeSensor))
        # self.assertTrue(isinstance(self.app.sleeper, Sleeper))

    def test_creates_range_sensor(self):
        self.assertIsNotNone(self.app.rangeSensor)

    @mock.patch("SumpOverflowAlert.App.time")
    def test_should_sleep_100_between_measurements(self, mock_time):
        def get_distance_stub():
            self.app.shouldContinue = self.shouldContinue()
            self.loop_count += 1
            return self.current_distance

        self.mock_time = mock_time
        self.sensor_mock.get_distance.side_effect = get_distance_stub

        self.app.run()

        mock_time.sleep.assert_called_with(0.1)

    @mock.patch("SumpOverflowAlert.App.time")
    def test_should_alert_after_previous_all_clear(self, mock_time):
        def get_distance_stub():
            self.app.shouldContinue = self.shouldContinue()
            self.loop_count += 1
            if self.loop_count % 200 == 0:
                self.current_distance = config.trigger_distance
            if self.loop_count % 200 == 1:
                self.current_distance = 0
            return self.current_distance

        self.mock_time = mock_time
        self.sensor_mock.get_distance.side_effect = get_distance_stub
        self.notifier_mock.send_notification.side_effect = self.sendNotificationStub
        self.notifier_mock.send_all_clear.side_effect = self.sendAllClearStub

        self.app.run()

        self.assertGreaterEqual(self.notifier_mock.send_notification.call_count, 2)
        self.assertGreaterEqual(self.notifier_mock.send_all_clear.call_count, 2)