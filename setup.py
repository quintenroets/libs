from setuptools import setup, find_packages
from libs.cli import Cli

NAME = "libs"

def read(filename):
    try:
        with open(filename) as fp:
            content = fp.read().split("\n")
    except FileNotFoundError:
        content = []
    return content


setup(
    author="Quinten Roets",
    author_email="quinten.roets@gmail.com",
    description='',
    name=f"quintenroets.{NAME}",
    version='1.0',
    packages=find_packages(),
    install_requires=read("requirements.txt"),
    entry_points={
        "console_scripts": [
            "konsolerun = libs.cli:main"
        ]},
)

Cli.install(*read("packages.txt"))
