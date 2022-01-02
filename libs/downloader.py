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
                    if i + 1 == max_tries:
                        raise requests.exceptions.RequestException
        
        if Downloader.check_content(temp_dest):
            temp_dest.rename(dest)

    @staticmethod
    def _download(url, dest, progress, headers={}, chunck_size=10**5, timeout=10, session=None, callback=None, **kwargs):
        if session is None:
            session = requests
        
        headers["Range"] = f"bytes={dest.size()}-"
        
        stream = session.get(url, headers=headers, timeout=timeout, stream=True)
        if stream.status_code == 416:
            headers.pop("Range")
            stream = session.get(url, headers=headers, timeout=timeout, stream=True)
            download_size = int(stream.headers["Content-Length"])
            start = 0
            end = download_size - 1
        
        else:
            if "Content-Range" not in stream.headers:
                raise requests.exceptions.RequestException
            
            content_range = stream.headers["Content-Range"].split(" ")[1]
            start_end, download_size = content_range.split("/")
            start, end = start_end.split("-")
            start, end, download_size = int(start), int(end), int(download_size)
        
        if progress.total is None:
            progress.total = download_size
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

        if start + download_size != dest.size():
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
