class Proxy:
    def __init__(self, handler):
        self.__handle__ = handler
        self.__handler__ = None

    def __getattr__(self, name):
        if self.__handler__ is None:
            self.__handler__ = self.__handle__()
        return self.__handler__.__getattribute__(name)
