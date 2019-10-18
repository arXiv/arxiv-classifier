import time


class Ticker:
    def __init__(self):
        """
        A simple logging clock.
        """
        self.time0 = time.time()
        self.time = self.time0

    def tick(self, label=''):
        now = time.time()
        dt = now - self.time
        self.time = now

        print('{}: {:0.2f} dt / {:0.2f} total'.format(
            label, dt, self.time - self.time0)
        )

    def __del__(self):
        print('Elapsed time: {}'.format(time.time() - self.time0))
