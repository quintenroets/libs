class Parser:
    @staticmethod
    def between(string, start=None, stop=None):
        start_pos = string.find(start) + len(start) if start else 0
        stop_pos = string.find(stop, start_pos) if stop else len(string)
        return string[start_pos: stop_pos]

    @staticmethod
    def rbetween(string, start=None, stop=None, reverse=False):
        stop_pos = string.rfind(stop) if stop else len(string) if stop else len(string)
        start_pos = string.rfind(start, 0, stop_pos) + len(start) if start else 0
        return string[start_pos: stop_pos]

    @staticmethod
    def after(string, start):
        start_pos = string.find(start)
        start_pos = start_pos + len(start) if start_pos >= 0 else 0
        return string[start_pos:]
