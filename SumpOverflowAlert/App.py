from SumpOverflowAlert import config
from SumpOverflowAlert.Notification.GmailNotifier import GmailNotifier
from SumpOverflowAlert.Sensor.RangeSensor import RangeSensor
from SumpOverflowAlert.sleeper import Sleeper

__author__ = 'John Sonneville'


class App(object):
    def __init__(self,
                 range_sensor=RangeSensor(),
                 gmail_notifier=GmailNotifier(config.gmail['username'], config.gmail['password']),
                 sleeper=Sleeper()):
        super().__init__()
        self.shouldContinue = True
        self.rangeSensor = range_sensor
        self.notifier = gmail_notifier
        self.sleeper = sleeper

    def run(self):
        sleep_timer = 0.1
        while self.shouldContinue:
            self.sleeper.sleep(sleep_timer)
            distance = self.rangeSensor.get_distance()
            if distance < config.trigger_distance:
                sleep_timer = 0.01
            else:
                sleep_timer = 0.1

                # self.notifier.send_notification()
                # else
                #     reduce duration
                # OR send alert
                # sleep(self.duration)

