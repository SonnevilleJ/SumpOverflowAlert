from time import sleep
from SumpOverflowAlert import config
from SumpOverflowAlert.Notification.GmailNotifier import GmailNotifier
from SumpOverflowAlert.Sensor.RangeSensor import RangeSensor

__author__ = 'John Sonneville'


class App(object):
    def __init__(self, sensor=RangeSensor):
        super().__init__()
        self.shouldContinue = True
        self.rangeSensor = sensor
        self.notifier = GmailNotifier(config.gmail['username'], config.gmail['password'])

    def run(self):

        sleep_timer = 0.1

        while self.shouldContinue:
            sleep(sleep_timer)
            distance = self.rangeSensor.get_distance()
            if distance < config.trigger_distance:
                sleep_timer = 0.01
                # else
                #     reduce duration
                # OR send alert
                # sleep(self.duration)

