from SumpOverflowAlert import config
from SumpOverflowAlert.Notification.GmailNotifier import GmailNotifier
from SumpOverflowAlert.Sensor.RangeSensor import RangeSensor

__author__ = 'John Sonneville'


class App(object):
    def __init__(self):
        super().__init__()
        self.rangeSensor = RangeSensor()
        self.notifier = GmailNotifier(config.gmail['username'], config.gmail['password'])
