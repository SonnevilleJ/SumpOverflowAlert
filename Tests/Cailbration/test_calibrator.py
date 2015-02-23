import sys

sys.path.append('./')

from unittest import TestCase
from SumpOverflowAlert.Calibration.Calibrator import Calibrator
from SumpOverflowAlert import config


class TestCalibrator(TestCase):
    def __init__(self, method_name='runTest'):
        super().__init__(method_name)

    def setUp(self):
        config.trigger_distance = 2
        self.initial_config_value = config.trigger_distance
        self.calibrator = Calibrator()

    def testShouldSetLevelToConfigTriggerDistance(self):
        self.assertEqual(self.calibrator.trigger_distance, config.trigger_distance)
        self.assertFalse(hasattr(self.calibrator, 'near_distance'))
        self.assertFalse(hasattr(self.calibrator, 'far_distance'))

    def testShouldSetNearAndFarToFirstValue(self):
        self.calibrator.record_observation(10)

        self.assertEqual(10, self.calibrator.near_distance)
        self.assertEqual(10, self.calibrator.far_distance)
        self.assertConfigWasNotChanged()

    def testShouldRecordNewNearDistance(self):
        self.calibrator.record_observation(5)

        self.calibrator.record_observation(4)

        self.assertEqual(self.calibrator.near_distance, 4)
        self.assertEqual(self.calibrator.far_distance, 5)
        self.assertConfigWasNotChanged()

    def testShouldNotChangeNearWhenRecordingFartherValue(self):
        self.calibrator.record_observation(6)
        self.calibrator.record_observation(7)

        self.assertEquals(self.calibrator.near_distance, 6)
        self.assertEqual(self.calibrator.far_distance, 7)
        self.assertEqual(self.initial_config_value, self.calibrator.trigger_distance)
        self.assertConfigWasNotChanged()

    def testShouldUpdateTriggerDistanceWhenCloserToFarThanNear(self):
        self.calibrator.record_observation(3)
        self.calibrator.record_observation(10)

        self.calibrator.record_observation(7)

        self.assertGreater(self.calibrator.trigger_distance, self.initial_config_value)
        self.assertConfigWasNotChanged()

    def testShouldNotReduceNearPastTriggerDistance(self):
        self.calibrator.record_observation(3)
        self.calibrator.record_observation(10)

        self.calibrator.record_observation(1)

        self.assertGreaterEqual(self.calibrator.trigger_distance, self.initial_config_value)
        self.assertGreaterEqual(self.calibrator.near_distance, self.calibrator.trigger_distance)
        self.assertConfigWasNotChanged()

    def testGetTriggerDistanceShouldReturnTriggerDistance(self):
        trigger_distance = self.calibrator.get_trigger_distance()

        self.assertEqual(config.trigger_distance, trigger_distance)

    def assertConfigWasNotChanged(self):
        self.assertEqual(self.initial_config_value, config.trigger_distance)