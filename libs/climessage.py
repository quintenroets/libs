class CliMessage:
    def __init__(self, message=None):
        self.message = message

    def __enter__(self, message=None):
        print(self.message, end="\r")

    def __exit__(self, exception_type, exception_value, exception_traceback):
        print("\r", end="")
        print(" " * (len(self.message) + 5), end="\r")

def ask(question, **choice_mappers):
    if not choice_mappers:
        choice_mappers = {
            True: ["", "yes", "y"],
            False: ["no", "n"]
        }
        question += " [Y/n] "

    print(question, end="")
    choice = input().lower().strip()
    for mapping, answers in choice_mappers.items():
        if choice in answers:
            choice = mapping
    return choice
