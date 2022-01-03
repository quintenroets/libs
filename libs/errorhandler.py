class ErrorHandler():
    error = False

    def __init__(self, obj=None):
        self.obj = obj
    
    def __enter__(self):
        pass

    def __exit__(self, type, value, tb):
        if tb:
            if type != KeyboardInterrupt and not ErrorHandler.error:
                ErrorHandler.show_error()
            if self.obj is not None:
                self.obj.crashed = str(tb)

        return True

    @staticmethod
    def show_error(message="", exit=True):
        # most of the time no error => save time by only importing on error
        
        import os
        import traceback

        from libs.cli import Cli
        from spathlib import Path
        
        ErrorHandler.error = True
        path = Path.assets / ".error.txt"
        if message:
            path.write_text(message)
        else:
            with open(path, "w") as fp:
                traceback.print_exc(file=fp)

        p = Cli.run(f'cat {path}; read', console=True, shell=True)

        if exit:
            with p:
                p.communicate() # make sure error message subprocess has started before terminating original process
                os._exit(0)

        return path.read_text()
