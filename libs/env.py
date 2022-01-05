from dotenv import load_dotenv
from plib import Path


def load(path=None):
    if path is None:
        path = Path.HOME / ".bash_profile"
    load_dotenv(dotenv_path=path)
    
