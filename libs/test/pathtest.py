from libs.path import Path
from libs.timer import Timer

with Timer():
    def match(path):
        return path.is_dir() and (path / ".git").exists()
    
    for _ in Path.docs.find(match, only_folders=True):
        pass 
