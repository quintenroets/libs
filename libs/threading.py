import cli

from threading import Thread as BaseThread

class Thread(BaseThread):
    def __init__(self, target, *args, exit_on_error=True, **kwargs):
        self.crashed = False
        self.exit_on_error = exit_on_error
        super(Thread, self).__init__(target=self.start_errorsafe, args=(target, *args), kwargs=(kwargs))
        
    def start_errorsafe(self, target, *args, **kwargs):
        with cli.errorhandler(self, exit=self.exit_on_error):
            target(*args, **kwargs)

    def start(self):
        super(Thread, self).start()
        return self

    def join(self):
        super(Thread, self).join()
        if self.crashed:
            raise Exception(self.crashed)



class Threads:
    def __init__(self, methods, *args, **kwargs):
        if type(methods) == list:
            self.threads = [Thread(m).start() for m in methods]
        else:
            self.threads = [Thread(methods, *arg, **kwargs).start() for arg in zip(*args)]

    def join(self):
        for t in self.threads:
            t.join()
