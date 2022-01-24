import time
import datetime


class Timer:
    total = 0

    def __init__(self, message=None, full=False, silent=False):
        self.message = message or "{}"
        self.full = full
        self.silent = silent

    def __enter__(self, message=None):
        self.start = time.time()

    def __exit__(self, exception_type, exception_value, exception_traceback):
        seconds = time.time() - self.start
        Timer.total += seconds  # keep global counter as well

        if not self.silent:
            interval_full = str(datetime.timedelta(seconds=seconds))
            interval = interval_full[:-3]
            if (
                seconds < 1 / 1000 or self.full
            ):  # only show nanoseconds when no milliseconds
                interval += f"'{interval_full[-3:]}"

            message = (
                self.message.format(interval)
                if "{}" in self.message
                else f"{self.message}: {interval}"
            )
            print(message)
