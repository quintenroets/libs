import itertools
import os
import subprocess
import sys
import time
import types

class Cli:
    @staticmethod
    def run(*commands, **kwargs):
        commands = Cli.check_iterable(*commands)
        chunck_size = 1 if "console" in kwargs and len(commands) > 1 else 100
        result = [Cli._run(commands[i: i + chunck_size], **kwargs) for i in range(0, len(commands), chunck_size)]
            
        if "console" in kwargs:
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
    def _run(commands, wait=True, console=False, confirm=False, debug=False, **kwargs):
        if "capture_output" not in kwargs:
            kwargs["stdout"] = sys.stdout

        if "check" not in kwargs and wait and not console:
            kwargs["check"] = True

        if not wait:
            # add empty element to finish total command with &
            commands = [f"nohup {c} &>/dev/null " for c in commands] + [""]

        if any(["sudo" in c for c in commands]) and not console:
            # Give password programatically
            pw = os.environ.get("pw")
            if pw is not None:
                start_command = f"echo {pw} | sudo -S echo "" &> /dev/null"
                commands = itertools.chain([start_command], commands)
                
        if confirm:
            commands = itertools.chain(commands, ["echo $'\nPress enter to quit.'", "read"])

        joiner = "; " if wait else "& "
        commands = ["/bin/bash", "-c", joiner.join(commands)]
        if console or debug:
            console = "konsole"
            commands = [console, "--new-tab", "-e"] + commands
            if debug:
                commands.insert(commands.index(console) + 1, "--noclose")
        
        run = subprocess.Popen if console else subprocess.run
        return run(commands, **kwargs)

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
    
def main():
    from libs.errorhandler import ErrorHandler
    
    with ErrorHandler():
        command = " ".join(sys.argv[1:])
        Cli.run(command, console=True)

if __name__ == "__main__":
    main()
