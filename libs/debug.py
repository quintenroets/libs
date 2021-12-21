import sys

class Debugger():
    def __init__(self, func=None, *args, **kwargs):
        self.func = func
        self.args = args
        self.kwargs = kwargs
        self.log_list = []
        
    def log(self, frame, event, arg):
        globals_vars = frame.f_globals
        globals_vars.pop("__builtins__")
        globals_vars.pop("__cached__")
        variables = {
            "locals": frame.f_locals,
            "globals": globals_vars,
            }
        self.log_list.append(variables)
        
    def callback(self, *args):
        if self.func:
            self.func(*self.args, **self.kwargs)
        else:
            self.log(*args)

    def __enter__(self):
        sys.settrace(self.callback)
        return self

    def __exit__(self, ext_type, exc_value, traceback):
        sys.settrace(None)
