""" Track the clock time elapsed since the last update """

import time

class TimeDelta(object):

    def __init__(self):

        self.last_reset = None

    def reset(self):
        self.last_reset = time.time()
        return self

    def delta(self):
        """ Returns the timedelta in seconds """
        return time.time() - self.last_reset

    def test(self, t):
        return self.last_reset + t < time.time()