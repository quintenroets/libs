import os
import subprocess
import sys
import tempfile

class Output:
    def __init__(self):
        self._stdout = None
        self._stderr = None
        self.file_object = None
        self.output = None

    def __enter__(self):
        self.file_object = tempfile.NamedTemporaryFile()
        self.file_object.__enter__()
        tee = subprocess.Popen(['tee', self.file_object.name], stdin=subprocess.PIPE)
        tee_fileno = tee.stdin.fileno()
        
        self._stdout = os.dup(1)
        self._stderr = os.dup(2)

        os.dup2(tee_fileno, sys.stdout.fileno())
        os.dup2(tee_fileno, sys.stderr.fileno())
        return self

    def __exit__(self, type_, value, traceback):
        os.dup2(self._stdout, 1)
        os.dup2(self._stderr, 2)
        self.output = str(self)
        self.file_object.__exit__(type_ ,value, traceback)

    def __str__(self):
        output = ''
        if self.output is not None:
            output = self.output
        elif self.file_object is not None:
            with open(self.file_object.name) as fp:
                output = fp.read()
        return output
