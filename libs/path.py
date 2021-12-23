import yaml

from pathlib import Path

yaml_suffix = ".yaml"

"""
Monkey-patch extra functionality onto pathlib
"""

Path.docs = Path.home() / "Documents"
Path.scripts = Path.docs / "Scripts"
Path.assets = Path.home() / ".config" / "scripts"


def _subpath(path: Path, *subnames, suffix=None):
    """
    Returns new path with subnames and suffix added
    """
    for name in subnames:
        path /= name
    if suffix is not None and path.suffix != suffix:
        path = path.with_suffix(suffix)
    return path

Path.subpath = _subpath


def _save(path: Path, content, *subnames):
    """
    Exports content to path in yaml format
    """
    path = path.subpath(*subnames, suffix=yaml_suffix)
    try:
        with open(path, "w") as fp:
            res = yaml.dump(content, fp)
    except FileNotFoundError:
        path.touch()
        res = path.save(content)
    return res

Path.save = _save


def _load(path: Path, *subnames):
    """
    Load content from path in yaml format
    """
    path = path.subpath(*subnames, suffix=yaml_suffix)
    try:
        with open(path) as fp:
            content = yaml.load(fp, Loader=yaml.SafeLoader)
    except FileNotFoundError:
        content = {}

    return content

Path.load = _load
