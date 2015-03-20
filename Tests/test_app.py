import sys

sys.path.append('./')

from unittest import TestCase
from unittest.mock import Mock, patch

import SumpOverflowAlert
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
        self.calibrator_mock = Mock()
        self.calibrator_mock.get_trigger_distance.side_effect = self.get_trigger_distance_stub
        self.app = App(self.sensor_mock, self.notifier_mock, self.calibrator_mock)

    def shouldContinue(self):
        return self.loop_count < self.max_loops

    def test_default_constructor_values(self):
        app = App()

        self.assertEqual(app.notifier.username, config.gmail['username'])
        self.assertEqual(app.notifier.password, config.gmail['password'])
        self.assertIsInstance(app.rangeSensor, SumpOverflowAlert.Sensor.RangeSensor.RangeSensor)
        self.assertIsInstance(app.calibrator, SumpOverflowAlert.Calibration.Calibrator.Calibrator)

    @patch("SumpOverflowAlert.App.time")
    def test_should_sleep_100_between_measurements(self, mock_time):
        def get_distance_stub():
            self.app.shouldContinue = self.shouldContinue()
            self.loop_count += 1
            return self.current_distance

        self.mock_time = mock_time
        self.sensor_mock.get_distance.side_effect = get_distance_stub
        self.calibrator_mock.trigger_distance = config.trigger_distance

        self.app.run()

        mock_time.sleep.assert_called_with(0.1)
        self.calibrator_mock.record_observation.assert_called_with(self.current_distance)
        self.calibrator_mock.get_trigger_distance.assert_called_with()

    def get_trigger_distance_stub(self):
        return config.trigger_distance

    def test_should_send_second_alert_after_all_clear(self):
        self.first_alert_triggered = False
        self.first_all_clear_triggered = False
        self.second_alert_triggered = False
        self.second_all_clear_triggered = False
        config.alert_after += 0.0001

        def get_distance_stub():
            if (self.first_alert_triggered and self.first_all_clear_triggered and not self.second_alert_triggered) or not self.first_alert_triggered:
                return config.trigger_distance - 1
            return config.trigger_distance + 1
        
        def send_notification_stub():
            if not self.first_alert_triggered:
                self.first_alert_triggered = True
            if self.first_alert_triggered and self.first_all_clear_triggered:
                self.second_alert_triggered = True

        def send_all_clear_stub():
            if self.first_all_clear_triggered:
                self.second_all_clear_triggered = True
                self.app.shouldContinue = False
            self.first_all_clear_triggered = True

        self.sensor_mock.get_distance.side_effect = get_distance_stub
        self.notifier_mock.send_notification.side_effect = send_notification_stub
        self.notifier_mock.send_all_clear.side_effect = send_all_clear_stub
        
        self.app.run()
        
        self.assertTrue(self.second_alert_triggered)
        self.assertTrue(self.second_all_clear_triggered)
        self.calibrator_mock.get_trigger_distance.assert_called_with()
