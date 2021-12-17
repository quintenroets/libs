from datetime import datetime

class Timer:
    def __init__(self, message=None):
        self.message = message

    def __enter__(self, message=None):
        self.start = datetime.now()

    def __exit__(self, exception_type, exception_value, exception_traceback):
        time = datetime.now() - self.start
        time = str(time)[:-3]
        message = self.message.format(time) if self.message else time
        print(message)
