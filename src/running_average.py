class RunningAverage:

    def __init__(self):
        self.reset()

    def reset(self):
        self.value = 0.0
        self.count = 0

    def update(self, value):
        self.value = (self.count*self.value + value)/(self.count + 1)
        self.count += 1
