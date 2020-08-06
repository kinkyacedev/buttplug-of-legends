import time


class Pattern:
    def __init__(self, duration, values):
        self.start_time = time.time()
        self.current_value = 0
        self.duration = duration
        self.values = values
    
    def next(self):
        if time.time() > self.start_time + self.duration:
            return None
        self.current_value = (self.current_value + 1) % len(self.values)
        return self.values[self.current_value - 1]


class Wave(Pattern):
    def __init__(self, duration, intensity):
        val = [0, 0, 2, 7, 13, 21, 30, 40, 50, 60, 70, 79, 87, 93, 98, 100, 100, 98, 93, 87, 79, 70, 60, 50, 40, 30, 21,
               13, 7, 2]
        values = [i * intensity / 10000 for i in val]
        super().__init__(duration, values)


class Stop(Pattern):
    pass
