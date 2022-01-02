import integv
import requests
import urllib
from tqdm import tqdm

from libs.path import Path


class Downloader:
    @staticmethod
    def download(url, dest=None, max_tries=10, **kwargs):
        if dest is None:
            dest = create_dest(url)
        
        session = kwargs.get("session", requests)
        headers = kwargs.get("headers", {})
        timeout = kwargs.get("timeout", 10)
        
        temp_dest = dest.with_suffix(dest.suffix + ".part")
        temp_dest.touch(exist_ok=True)
        temp_dest.unlink()
        temp_dest.touch(exist_ok=True)
        
        total_size = session.get(url, headers=headers, timeout=timeout, stream=True).headers["Content-Length"]
        progress = tqdm(total=total_size, desc=f"Downloading {dest.name}")
        
        with progress:
            for _ in range(max_tries):
                try:
                    progress = Downloader._download(url, temp_dest, progress, session, **kwargs)
                    progress.close()
                    break
                except requests.exceptions.RequestException:
                    pass
        
        if check_content(temp_dest):
            temp_dest.rename(dest)
    
    @staticmethod
    def _download(url, dest, progress, headers={}, chunck_size=10**5, timeout=10, **kwargs):
        downloaded_size = dest.stat().st_size if dest.exists() else 0
        headers["Range"] = f"bytes={downloaded_size}-"
        
        stream = session.get(url, headers=headers, timeout=timeout, stream=True)
        
        if "Content-Range" not in stream.headers:
            print(stream)
            print(stream.headers)
            raise requests.exceptions.RequestException
        
        content_range = stream.headers.get("Content-Range")
        start = int(content_range.split(" ")[1].split("-")[0]) if content_range else 0
        
        old_filesize = dest.size()
        download_size = int(stream.headers["Content-Length"])
        
        with open(dest, "ab") as fp:
            fp.seek(start)
            
            for chunck in stream.iter_content(chunck_size):
                fp.write(chunck)
                progress.update(len(chunck))

        if download_size != dest.size() - old_filesize:
            raise requests.exceptions.RequestException


def check_content(filename):
    content = filename.read_bytes()
    try:
        succes = integv.verify(content, file_type=filename.suffix[1:])
    except NotImplementedError:
        succes = True
    return succes


def create_dest(url):
    path = urllib.parse.urlparse(url).path
    dest = urllib.parse.unquote(path).split("/")[-1]
    dest = Path(dest)
    return dest
