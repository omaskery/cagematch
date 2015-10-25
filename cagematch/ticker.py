"""this file implements a utility for running event repeatedly with a certain interval"""
import datetime


class Ticker(object):
    """ticker is used to 'tick' (run an operation) at a fixed time interval"""
    def __init__(self, period):
        self._period = period
        self._last_examined = datetime.datetime.now()
        self._delta_ticks = 0
        self._next_tick = datetime.datetime.now()

    @staticmethod
    def from_seconds(seconds):
        """construct a ticker by giving it the number of seconds between 'ticks'"""
        return Ticker(datetime.timedelta(seconds=seconds))

    @staticmethod
    def from_frequency(frequency):
        """construct a ticker by giving it the frequency of 'ticks'"""
        period = datetime.timedelta(seconds=1.0/frequency)
        return Ticker(period)

    def tick(self, behaviour=lambda: None, accumulate=True):
        """asks the ticker to tick if the interval has expired, returning whether
        the interval had expired - takes an optional behaviour function that will
        be executed if the interval expired. Accumulate parameter is used to specify
        whether the next event is scheduled based on when current tick should have
        occurred, or scheduled based on when the current tick did happen."""
        now = datetime.datetime.now()
        ticked = False
        # is it time to tick yet?
        if now >= self._next_tick:
            # we need to schedule the next tick:
            if accumulate:
                # if we accumulate error, then just move the time for the next tick forward
                # by the period amount
                self._next_tick += self._period
            else:
                # if we do not accumulate error, then just set the next tick for now + period
                self._next_tick = now + self._period
            self._delta_ticks += 1
            behaviour()
            ticked = True
        return ticked

    def ticks_per_second(self):
        """asks the ticker how many ticks per second is has done (on average)
        since this function (ticks_per_second()) was last called"""
        now = datetime.datetime.now()
        delta_time = now - self._last_examined
        result = self._delta_ticks / delta_time.total_seconds()
        self._delta_ticks = 0
        self._last_examined = now
        return result
