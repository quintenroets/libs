import yaml

from pathlib import Path

yaml_suffix = ".yaml"

"""
Monkey-patch extra functionality onto pathlib
"""

Path.docs = Path.home() / "Documents"
Path.scripts = Path.docs / "Scripts"
Path.assets = Path.home() / ".config" / "scripts"


def _subpath(path: Path, *names, suffix=None):
    """
    Returns new path with subnames and suffix added
    """
    for name in names:
        path /= name
    if suffix is not None and path.suffix != suffix:
        path = path.with_suffix(suffix)
    return path


def _save(path: Path, content, *names):
    """
    Exports content to path in yaml format
    """
    path = path.subpath(*names, suffix=yaml_suffix)
    try:
        with open(path, "w") as fp:
            res = yaml.dump(content, fp)
    except FileNotFoundError:
        path.touch()
        res = path.save(content)
    return res


def _load(path: Path, *names):
    """
    Load content from path in yaml format
    """
    path = path.subpath(*names, suffix=yaml_suffix)
    try:
        with open(path) as fp:
            content = yaml.load(fp, Loader=yaml.SafeLoader)
    except FileNotFoundError:
        content = {}

    return content


def _find(path: Path, condition=None, recurse_on_match=False, follow_symlinks=True):
    """
    Find all subpaths under path that match condition
    """
    if condition is None:
        def condition(_):
            return True

    to_traverse = [path]
    while to_traverse:
        path = to_traverse.pop(0)
        match = condition(path)
        if match:
            yield path
        if not match or recurse_on_match:
            for child in path.iterdir():
                if child.is_dir():
                    if follow_symlinks or not child.is_symlink():
                        to_traverse.append(child)


Path.subpath = _subpath
Path.save = _save
Path.load = _load
Path.find = _find