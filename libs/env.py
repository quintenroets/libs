from dotenv import load_dotenv
from .path import Path


def load():
    load_dotenv(dotenv_path=Path.HOME / ".bash_profile")
    
