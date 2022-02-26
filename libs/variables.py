import inspect
import types

from rich import pretty

vars = {}


def save_locals():
    local_vars = inspect.stack()[1].frame.f_locals  # locals of one function above
    local_vars = {k: v for k, v in local_vars.items() if not k.startswith("_")}
    vars.update(local_vars)


def get_locals():
    return vars


def insert_locals():
    for k, v in get_locals().items():
        globals()[k] = v


def show_globals():
    exclude_types = [types.ModuleType, types.FunctionType]
    global_vars = {
        k: v
        for k, v in globals().items()
        if not k.startswith("_")
        and not (any([isinstance(v, e) for e in exclude_types]))
    }
    pretty.pprint("Globals: ")
    pretty.pprint(global_vars)
