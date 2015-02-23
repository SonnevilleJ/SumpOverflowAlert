from SumpOverflowAlert import config


class Calibrator(object):
    def __init__(self):
        super().__init__()
        self.trigger_distance = config.trigger_distance
        self.has_recorded_anything = False

    def record_observation(self, level):
        if not self.has_recorded_anything:
            self.near_distance = level
            self.far_distance = level
            self.has_recorded_anything = True
        else:
            if self.near_distance > level > self.trigger_distance:
                self.near_distance = level
            if level > self.far_distance:
                self.far_distance = level
            else:
                if level - self.near_distance > self.far_distance - level:
                    self.trigger_distance = self.near_distance

    def get_trigger_distance(self):
        return self.trigger_distance