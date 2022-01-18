import dbus
import itertools
import time
import fnmatch, os, subprocess, time
import tbhandler.threading as threading

session_bus = dbus.SessionBus()

def get_dbus_interface(name, path, interface):
    obj = session_bus.get_object(name, path)
    return dbus.Interface(obj, dbus_interface=interface)


class Popup:
    def __init__(self,
            *args,
            title='Working',
            message='',
            progress_name='',
            amount=0,
            description=False,
            show_progress_message=True,
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

        app_icon_name = ''
        ui_interface = get_dbus_interface('org.kde.kuiserver', '/JobViewServer', 'org.kde.JobViewServer')
        own_interface_path = ui_interface.requestView(title, app_icon_name, 0)
        
        handle = get_dbus_interface('org.kde.kuiserver', own_interface_path, 'org.kde.JobViewV2')
        handle.setInfoMessage(message)
        if amount != 0:
            handle.setPercent(1)
            self.percentage = 1
        self.handle = handle
        if description:
            self.handle.setDescriptionField(0, '', self.message)
    
    def __enter__(self):
        return self

    def __exit__(self, _, exception, tb):
        self.set_progress(self.progress_value)
        self.finished = True

        if not exception:
            message = ''
        elif isinstance(exception, KeyboardInterrupt):
            message = 'Cancelled'
        else:
            message = 'Error'
            
        self.handle.setInfoMessage('')
        self.handle.terminate(message)
        
    def progress(self):
        self.set_progress(self.progress_value + 1)
        
    def set_progress(self, progress):
        self.progress_value = progress
        self.show_progress()
        
    def show_progress(self, percentage=None):
        if self.amount != 0 and self.amount is not None:
            if not percentage:
                percentage = 100 * self.progress_value / self.amount
            # Don't go backwards
            percentage = max(percentage, self.percentage)
            percentage = min(percentage, 100)
            self.handle.setPercent(percentage)
            self.set_progress_message()

    def add_progress(self, progress):
        self.set_progress(self.progress_value + progress)

    def set_progress_message(self):
        message = f'{self.message}' if self.message else ''
        if self.show_progress_message:
            message = f'{message}\n{self.progress_value}/{self.amount} {self.progress_name}'
        if self.handle:
            self.handle.setInfoMessage(message)

    def set_message(self, message):
        self.message = message
        self.set_progress_message()

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
