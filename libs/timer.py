import time
from datetime import timedelta
from functools import wraps
from typing import Callable

import cli


class Timer:
    total = 0

    def __init__(self, message=None, full=False, silent=False):
        self.message = message or "{}"
        self.full = full
        self.silent = silent

    def __enter__(self, message=None):
        self.start = time.perf_counter()

    def __exit__(self, exception_type, exception_value, exception_traceback):
        seconds = time.perf_counter() - self.start
        Timer.total += seconds  # keep global counter as well

        if not self.silent:
            interval_full = str(timedelta(seconds=seconds))
            interval = interval_full[:-3]
            if seconds < 1 / 1000 or self.full:
                microseconds_message = interval_full[-3:]
                interval += f"'{microseconds_message}"

            message = (
                self.message.format(interval)
                if "{}" in self.message
                else f"{self.message}: {interval}"
            )
            cli.console.print(message)


def timing(function: Callable):
    """
    Returns a timing decorator.
    Times duration of function
    """

    @wraps(function)
    def timing_decorator(*args, **kwargs):
        with Timer(function.__name__):
            return function(*args, **kwargs)

    return timing_decorator
