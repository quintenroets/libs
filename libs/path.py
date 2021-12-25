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


def _find(path: Path, condition=None, exclude=None, recurse_on_match=False, follow_symlinks=True, only_folders=False):
    """
    Find all subpaths under path that match condition

    only_folders can be used for efficiency reasons
    """
    if condition is None:
        recurse_on_match = True
        def condition(_):
            return True

    if exclude is None:
        def exclude(_):
            return False

    to_traverse = [path]
    while to_traverse:
        path = to_traverse.pop(0)
        
        if not exclude(path):
            match = condition(path)
            if match:
                yield path

            if not match or recurse_on_match:
                if only_folders or path.is_dir():
                    for child in path.iterdir():
                        if follow_symlinks or not child.is_symlink():
                            if not only_folders or child.is_dir():
                                to_traverse.append(child)


Path.subpath = _subpath
Path.save = _save
Path.load = _load
Path.find = _find
