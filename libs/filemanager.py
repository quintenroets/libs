import os
import json
import yaml
import pickle

from libs.cli import Cli
from libs import folders

class FileManager:
    default_extension = "yaml"
    root = folders.home / ".config" / "scripts"

    @classmethod
    def load(cls, *path, mode="r", folder=False, add_ext=True):
        path = cls.get_path(*path, folder=folder or not add_ext)
        is_dict = path.endswith(".json") or path.endswith(".yaml")
        if path.endswith(".pkl"):
            mode = "rb"

        try:
            with open(path, mode) as fp:
                if path.endswith(".yaml"):
                    content = yaml.load(fp, Loader=yaml.FullLoader)
                elif path.endswith(".json"):
                    content = json.load(fp)
                elif path.endswith(".pkl"):
                    content = pickle.load(fp)
                else:
                    content = fp.read()

        except FileNotFoundError:
            content = {} if is_dict else (b"" if mode == "rb" else "")

        if content is None and is_dict:
            content = {}

        return content

    @classmethod
    def save(cls, content, *path, encoding=None, folder=False, add_ext=True):
        path = cls.get_path(*path, create=True, folder=folder or not add_ext)
        
        mode = "w"
        if not path.endswith(".yaml") and not path.endswith(".json"):
            if isinstance(content, bytes) or path.endswith(".pkl"):
                mode = "wb"

        try:
            with open(path, mode=mode, encoding=encoding) as fp:
                cls.save_content(path, fp, content)
        except PermissionError:
            # write via other file
            local_path = os.path.basename(path)
            with open(local_path, mode=mode, encoding=encoding) as fp:
                cls.save_content(local_path, fp, content)
            from libs.cli import Cli
            Cli.run(f'sudo mv "{local_path}" "{path}"')

        return path

    @classmethod
    def save_content(cls, path, fp, content):
        if path.endswith(".yaml"):
            yaml.dump(content, fp)
        elif path.endswith(".json"):
            json.dump(content, fp, indent=4)
        elif path.endswith(".pkl"):
            pickle.dump(content, fp)
        else:
            fp.write(content)

    @classmethod
    def get_path(cls, *path, create=False, folder=False):
        if len(path) > 1 and not str(path[0]).startswith("/"):
            # don't replace slashes in absolute path
            path = [p.replace("/", "_") for p in path]
        else:
            path = list(path)
        if not str(path[0]).startswith("/"):
            path.insert(0, cls.root)
        
        if "." not in str(path[-1]) and not folder:
            path[-1] += "." + FileManager.default_extension

        path = os.path.join(*path)
        if create:
            created_folder = path if folder else os.path.dirname(path)
            try:
                os.makedirs(created_folder, exist_ok=True)
            except FileExistsError: # still throws error for root files
                pass
        
        return path
