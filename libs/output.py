import os
import sys
import tempfile
from threading import Lock

mutex = Lock()

class Output:
    def __init__(self, capture_errors=False):
        self._stdout = None
        self._stderr = None
        self.output = None
        self.output_value = None
        self.capture_errors = capture_errors

    def __enter__(self):
        self._stdout = sys.stdout
        self._stderr = sys.stderr
        self.output = tempfile.TemporaryFile(mode="w+")

        sys.stdout = self.output
        if self.capture_errors:
            sys.stderr = self.output
        return self

    def __exit__(self, type, value, traceback):
        self.output_value = str(self)
        self.output.close()
        sys.stdout = self._stdout
        sys.stderr = self._stderr

    def __str__(self):
        if self.output is None:
            output_value = ""
        elif self.output_value is None:
            with mutex:
                self.output.seek(0)
                output_value = self.output.read()
                self.output.seek(0, os.SEEK_END)
        else:
            output_value = self.output_value

        return output_value
