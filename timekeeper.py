import time

class TimerError(Exception):

    """A custom exception used to report errors in use of Timer class"""


class Timer:
    team_name = "UNKNOWN"

    def __init__(self, team_name):

        self._start_time = 0.0
        self._count = 0.0
        self.team_name = team_name

    def start(self):

        """Start a new timer"""

        if self._start_time != 0.0:

            raise TimerError(f"Timer is running. Use .stop() to stop it")


        self._start_time = time.perf_counter()

    def stop(self):

        """Stop the timer"""

        if self._start_time is None:

            raise TimerError(f"Timer is not running. Use .start() to start it")

        res = time.perf_counter() - self._start_time
        self._count += res
        self._start_time = 0.0
        return res

    def show(self):
        """Report the current Time"""
        # Get hours, minutes, seconds elapsed
        secs = self._count
        mins = 0.0
        hours = 0.0
        if secs >= 60.0:
            mins = secs/60
            # get rid of excess seconds (shouldn't be > 60)
            min_int = round(mins)
            subtract = min_int * 60
            secs = secs - subtract
        if mins >= 60.0:
            hours = mins/60
            hours_int = round(hours)
            subtract = hours_int * 60
            mins = mins - subtract


        # Get rid of the decimal values by rounding to nearest whole number - note that round() returns an int
        secs = round(secs)
        mins = round(mins)
        hours = round(hours)

        # format them to have leading zeros for all numbers with less than two digits
        secs = "{:02d}".format(secs)
        mins = "{:02d}".format(mins)
        hours = "{:02d}".format(hours)

        # Get the string representation of all of these values
        secs = str(secs)
        mins = str(mins)
        hours = str(hours)

        time = self.team_name + " (" + hours + ":" + mins + ":" + secs + ")"
        return time

""" TEST THE FUNCTIONALITY OF THE TIMEKEEPER """
if __name__ == "__main__":
    tester = Timer("WHITE")
    tester.start()
    time.sleep(64)
    tester.stop()
    print(tester.show())