import importlib
from pathlib import Path
import sys

from libs.debug import Debugger


class Reloader(Debugger):
    def __init__(self, root=None):
        super().__init__(self, reload, root=root)


def reload(root=None, auto=False):
    """
    Reload all imported modules with files under root:
    very handy to see changes without kernel restart
    """
    if root is None:
        root = Path.home()
    
    if auto:
        def auto_reload(*args):
            _reload(root=root)
        sys.settrace(auto_reload)
        
    else:
        return _reload(root)


def _reload(root=None):
    """
    Reload all imported modules with files under root:
    very handy to see changes without kernel restart
    """

    to_reload = [
        module
        for module in sys.modules.values()
        if module.__dict__.get("__file__")
        and root in Path(module.__dict__["__file__"]).parents
    ]
    reloaded = []

    for module in to_reload:
        load_time = get_load_time(module)
        module = importlib.reload(module)
        
        if get_load_time(module) > load_time:
            name = module.__dict__['__name__']
            reloaded.append(name)
            
    return reloaded


def get_load_time(module):
    load_time = 0
    load_file = module.__dict__.get("__cached__")
    if load_file:
        load_path = Path(load_file)
        if load_path.exists():
            load_time = load_path.stat().st_mtime
            
    return load_time
