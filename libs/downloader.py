import integv
import requests
import urllib
from tqdm import tqdm

from libs.path import Path


class Downloader:
    @staticmethod
    def download(url, dest=None, max_tries=10, **kwargs):
        if dest is None:
            dest = Downloader.create_dest(url)
                
        temp_dest = dest.with_suffix(dest.suffix + ".part")
        temp_dest.touch(exist_ok=True)
        
        progress = tqdm(desc=f"Downloading {dest.name}")
        
        with progress:
            for i in range(max_tries):
                try:
                    progress = Downloader._download(url, temp_dest, progress, **kwargs)
                    break
                except requests.exceptions.RequestException:
                    progress.set_description(f"Downloading {dest.name} (retry {i}/{max_tries - 1}")
        
        if Downloader.check_content(temp_dest):
            temp_dest.rename(dest)

    @staticmethod
    def _download(url, dest, progress, headers={}, chunck_size=10**5, timeout=10, session=None, callback=None, **kwargs):
        if session is None:
            session = requests
        
        old_filesize = dest.size()
        headers["Range"] = f"bytes={old_filesize}-"
        
        stream = session.get(url, headers=headers, timeout=timeout, stream=True)
        
        if "Content-Range" not in stream.headers:
            raise requests.exceptions.RequestException
        
        content_range = stream.headers.get("Content-Range")
        start = int(content_range.split(" ")[1].split("-")[0]) if content_range else 0
        
        if progress.total is None:
            progress.total = int(stream.headers["Content-Length"])
            progress.update(start)
            if callback:
                callback(start /progress.total)
        
        with open(dest, "ab") as fp:
            fp.seek(start)
            for chunck in stream.iter_content(chunck_size):
                fp.write(chunck)
                progress.update(len(chunck))
                if callback:
                    callback(len(chunck)/progress.total)

        download_size = int(stream.headers["Content-Length"])
        if download_size != dest.size() - old_filesize:
            raise requests.exceptions.RequestException

    @staticmethod
    def check_content(filename):
        content = filename.read_bytes()
        try:
            succes = integv.verify(content, file_type=filename.suffix[1:])
        except NotImplementedError:
            succes = True
        return succes

    @staticmethod
    def create_dest(url):
        path = urllib.parse.urlparse(url).path
        dest = urllib.parse.unquote(path).split("/")[-1]
        dest = Path(dest)
        return dest
