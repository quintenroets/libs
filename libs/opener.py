import os

from libs.cli import Cli

def startfile(file):
    if os.path.islink(file):
        file = readlink(file)
        
    Cli.run(f"xdg-open '{file}'", wait=False)
