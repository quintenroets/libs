import itertools
import os
import subprocess
import sys
import time
import types

from libs.errorhandler import ErrorHandler
from libs.output_copy import Output


class Cli:
    Error = subprocess.CalledProcessError
    
    @staticmethod
    def run(*commands, **kwargs):
        commands = Cli.check_iterable(*commands)
        chunck_size = 1 if "console" in kwargs and len(commands) > 1 else 100
        result = [Cli._run(commands[i: i + chunck_size], **kwargs) for i in range(0, len(commands), chunck_size)]
        
        if "capture_output" not in kwargs and len(result) == 1:
            result = result[0]
            
        if kwargs.get("console") and commands:
            # only activate console if console kwargs True and if commands have effectively run
            
            console = "konsole"
            is_open = Cli.get(
                f"wmctrl -l | grep ' '$(xdotool get_desktop)' ' | grep {console.capitalize()}",
                check=False
            )
            if not is_open:
                time.sleep(0.5)
            Cli.run(f"jumpapp -w {console}") # always focus new tabs but wait if first tab
                
        return result

    @staticmethod
    def _run(commands, wait=True, console=False, confirm=False, debug=False, shell=False, **kwargs):
        commands = list(commands) # we want to be able to loop multiple times
        if "capture_output" not in kwargs:
            kwargs["stdout"] = sys.stdout

        if "check" not in kwargs and wait and not console:
            kwargs["check"] = True

        if "pwd" in kwargs:
            pwd = kwargs.pop("pwd")
            commands.insert(0, f'cd "{pwd}"')

        if not wait:
            # add empty element to finish total command with &
            commands = [f"nohup {c} &>/dev/null " for c in commands] + [""]

        if any(["sudo" in c for c in commands]) and not console:
            # Give password programatically
            pw = os.environ.get("pw")
            
            if pw is None:
                from dotenv import load_dotenv # long import time and not often needed
                from plib import Path
                load_dotenv(dotenv_path=Path.HOME / ".bash_profile")
                pw = os.environ.get("pw")

            if pw is not None:
                start_command = f"echo {pw} | sudo -S echo "" &> /dev/null"
                commands.insert(0, start_command)
                
        if confirm:
            commands += ["echo -n $'Exit? [Y/n]'", "read"]

        joiner = "; " if wait else "& "
        commands = [joiner.join(commands)]
        
        if shell or any([bash_symbol in commands[0] for bash_symbol in " ;$"]):
            commands = [os.environ["SHELL"], "-c"] + commands
        
        if console or debug:
            commands = ["konsole", "--new-tab", "-e"] + commands
            if debug:
                commands.insert(commands.index(console) + 1, "--noclose")
            if "DISPLAY" not in os.environ:
                os.environ["DISPLAY"] = ":0.0" # needed for non-login scripts to be able to activate console
        
        run = subprocess.Popen if console else subprocess.run
        try:
            res = run(commands, **kwargs)
        except subprocess.CalledProcessError as e:
            if e.stderr is not None:
                raise Exception(e.stderr.decode())
            else:
                raise e

        return res

    @staticmethod
    def get(*commands, **kwargs):
        results = Cli.run(*commands, capture_output=True, **kwargs)
        result = "".join([r.stdout.decode().strip() for r in results])
        return result

    @staticmethod
    def install(*packages, installer_command=None):
        packages = Cli.check_iterable(*packages)
        
        installer_commands = {
            "apt": "apt install -y",
            "pacman": "pacman -S --noconfirm"
        }
        if installer_command is None:
            package_manager = Cli.get_package_manager()
            installer_command = installer_commands[package_manager]

        commands = [f"sudo {installer_command} {p}" for p in packages]
        return Cli.run(commands, check=False)

    @staticmethod
    def get_package_manager():
        for manager in ["apt", "pacman"]:
            if Cli.get(f"which {manager}", check=False):
                return manager
            
    @staticmethod
    def check_iterable(*args):
        if args:
            arg = args[0]
            if isinstance(arg, list) or isinstance(arg, tuple):
                args = arg
            elif isinstance(arg, types.GeneratorType):
                args = list(arg)
        return args
    
    @staticmethod
    def set_title(title):
        return Cli.run(f'qdbus org.kde.konsole $KONSOLE_DBUS_SESSION setTitle 1 "{title}"')

    @staticmethod
    def run_exe(path):
        Cli.run(f"./{path.name}", pwd=path.parent)


def main():
    with ErrorHandler():
        commands = sys.argv[1:]
        Cli.run(commands, console=True)


if __name__ == "__main__":
    main()
