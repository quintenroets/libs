import itertools


class CliProgress:
    def __init__(self,
            *args,
            title="Working",
            message="",
            progress_name="",
            amount=0,
            description=False,
            show_progress_message=True,
            capture_output=False,
            capture_errors=False
            ):

        # title can be given by first argument as well
        if args and isinstance(args[0], str):
            title, *args = args
        self.iterator = itertools.chain(*args) if args else None

        self.amount = amount
        if self.amount == 0 and args:
            try:
                self.amount = sum([len(arg) for arg in args])
            except TypeError:
                pass

        self.message = message
        self.progress_name = progress_name
        self.progress_value = 0
        self.percentage = 0
        self.show_progress_message = show_progress_message
        self.finished = False

        if amount != 0:
            self.percentage = 1

    
    def __enter__(self):
        return self

    def __exit__(self, _, exception, tb):
        self.set_progress(self.progress_value)
        self.finished = True
        
    def progress(self):
        self.set_progress(self.progress_value + 1)
        
    def set_progress(self, progress):
        self.progress_value = progress
        self.show_progress()
        
    def show_progress(self, percentage=None):
        pass

    def add_progress(self, progress):
        self.set_progress(self.progress_value + progress)

    def set_message(self, message):
        self.message = message

    def set_amount(self, amount):
        self.amount = amount

    def __iter__(self):
        with self:
            for item in self.iterator:
                yield item
                self.progress()
                
    def iterate(self, iterator):
        self.iterator = iterator
        return self.__iter__()
