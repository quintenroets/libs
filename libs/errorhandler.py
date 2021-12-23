from libs.path import Path

class ErrorHandler():
    error = False

    def __init__(self, obj=None):
        self.obj = obj
    
    def __enter__(self):
        pass

    def __exit__(self, type, value, tb):
        if tb:
            if type != KeyboardInterrupt:
                ErrorHandler.show_error()
            if self.obj is not None:
                self.obj.crashed = str(tb)

        return True

    @staticmethod
    def show_error(message="", exit=True):
        import traceback
        from libs.cli import Cli

        if not ErrorHandler.error:
            ErrorHandler.error = True
            path = Path.assets / ".error.txt"
            if message:
                path.write_text(message)
            else:
                with open(path, "w") as fp:
                    traceback.print_exc(file=fp)

            Cli.run(f'cat {path}; read', console=True)

            if exit:
                import os
                os._exit(0)

            return path.read_text()
