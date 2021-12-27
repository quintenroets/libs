from progress.spinner import Spinner
from threading import Thread
import time

class CliSpinner:
    def __init__(self, message=None):
        self.message = f"{message}.. "
        self.spinner = Spinner(self.message)
        self.quit = False

    def __enter__(self, message=None):
        Thread(target=self.update).start()
        
    def update(self):
        while not self.quit:
            self.spinner.next()
            time.sleep(0.1)

    def __exit__(self, exception_type, exception_value, exception_traceback):
        self.quit = True
        print("\r", end="")
        print(" " * (len(self.message) + 5), end="\r")
