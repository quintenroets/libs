from plib import Path

from libs.cli import Cli


class ShortcutMaker:
    def __init__(self):
        self.config_file = Path.HOME / ".xbindkeysrc.scm"
        edge = "; -- scripts --"
        self.header = self.config_file.read_text().split(edge)[0] + edge + "\n"
        self.items = []

    def set_shortcuts(self):
        new_content = "\n".join([
            "(set-keyboard-bindings",
            *self.items,
            ")"
        ])
        content = self.header + new_content
        self.config_file.write_text(content)
        Cli.run("xbindkeys --poll-rc")

    def make_shortcut(self, hotkey, target):
        item = f"\t(list '({hotkey}) \"{target}\")" if target else "\n"
        self.items.append(item) 
