from libs.filemanager import FileManager
from libs.cli import Cli


class ShortcutMaker:
    def __init__(self):
        edge = "; -- scripts --"
        self.header = FileManager.load(".xbindkeysrc.scm").split(edge)[0] + edge + "\n"
        self.items = []

    def set_shortcuts(self):
        new_content = "\n".join([
            "(set-keyboard-bindings",
            *self.items,
            ")"
        ])
        content = self.header + new_content
        FileManager.save(content, ".xbindkeysrc.scm")
        Cli.run("xbindkeys --poll-rc")

    def make_shortcut(self, hotkey, target):
        item = f"\t(list '({hotkey}) \"{target}\")" if target else "\n"
        self.items.append(item) 
