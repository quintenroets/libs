from dotenv import load_dotenv
from plib import Path


def load():
    load_dotenv(dotenv_path=Path.HOME / ".bash_profile")
    
