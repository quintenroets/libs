from plib import Path


def match(path):
    return (path / ".git").exists()


for _ in Path.docs.find(match, only_folders=True):
    pass
