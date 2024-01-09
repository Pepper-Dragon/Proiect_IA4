import time


class DeltaTimeClass:
    def __init__(self):
        self.deltaTime = 0
        self.prev_time = time.perf_counter()
        self.current_time = 0

    def update(self):
        self.current_time = time.perf_counter()
        self.deltaTime = self.current_time - self.prev_time
        self.prev_time = self.current_time

        #if self.deltaTime > 0.006:
        #    self.deltaTime = 0.006

    def getDeltaTime(self):
        return self.deltaTime


DeltaTime = DeltaTimeClass()