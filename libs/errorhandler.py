from libs.filemanager import FileManager

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
        import os
        from libs.cli import Cli

        if not ErrorHandler.error:
            ErrorHandler.error = True
            filename = FileManager.save(message, os.environ["scripts"], ".error.txt")
            if not message:
                with open(filename, "w") as fp:
                    traceback.print_exc(file=fp)

            Cli.run(f'cat {filename}; read', console=True)

            if exit:
                os._exit(0)

            with open(filename) as fp:
                return fp.read()
