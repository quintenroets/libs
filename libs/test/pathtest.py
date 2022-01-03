from path import Path
from libs.timer import Timer

with Timer():
    def match(path):
        return (path / ".git").exists()
    
    for _ in Path.docs.find(match, only_folders=True):
        pass 
