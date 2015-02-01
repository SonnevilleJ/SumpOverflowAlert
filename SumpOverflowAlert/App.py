from SumpOverflowAlert import config
from SumpOverflowAlert.Notification.GmailNotifier import GmailNotifier
from SumpOverflowAlert.Sensor.RangeSensor import RangeSensor
from sleeper import Sleeper

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
        loop_counter = 0
        notification_sent = False
        while self.shouldContinue:
            self.sleeper.sleep(sleep_timer)
            distance = self.rangeSensor.get_distance()
            loop_counter += 1
            if distance < config.trigger_distance:
                sleep_timer = 0.01
                if loop_counter * sleep_timer == config.alert_after:
                    self.notifier.send_notification()
                    notification_sent = True
            else:
                sleep_timer = 0.1
                if notification_sent:
                    self.notifier.send_all_clear()
                    notification_sent = False
                    loop_counter = 0

