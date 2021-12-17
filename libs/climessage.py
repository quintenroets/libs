class CliMessage:
    def __init__(self, message=None):
        self.message = message

    def __enter__(self, message=None):
        print(self.message, end="\r")

    def __exit__(self, exception_type, exception_value, exception_traceback):
        print(" " * len(self.message), end="\r")
