import types

def save(**kwargs):
    for k, v in kwargs.items():
        globals()[k] = v

def show():
    exclude_types = [types.ModuleType, types.FunctionType]
    global_vars = {
        k: v for k, v in globals().items()
        if not k.startswith("_")
        and not(any([isinstance(v, e) for e in exclude_types]))
    }
    message = "Variables: " + ", ".join(global_vars)
    print(message)
    return global_vars
