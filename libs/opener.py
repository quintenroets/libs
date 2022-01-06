import os

from libs.cli import Cli


def open_files(*filenames):
    if os.name == 'nt':
        for filename in filenames:
            os.startfile(filename)
    else:
        Cli.run((f'xdg-open "{filename}"' for filename in filenames), wait=False)
