import time
import datetime

class Timer:
    def __init__(self, message=""):
        self.message = message
        if self.message and "{}" not in self.message:
            self.message += ": "

    def __enter__(self, message=None):
        self.start = time.time()

    def __exit__(self, exception_type, exception_value, exception_traceback):
        seconds = time.time() - self.start
        if seconds > 1:
            seconds = round(seconds, 3)
        
        interval = datetime.timedelta(seconds=seconds)
        interval = str(interval)
                    
        #while interval[0] in "0:" and interval[1] != ".":
        #interval = interval[1:]
                    
        while interval[-1] == "0":
            interval = interval[:-1]
        
        message = self.message.format(interval) if "{}" in self.message else f"{self.message}{interval}"
        print(message)
