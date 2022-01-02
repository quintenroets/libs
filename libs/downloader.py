import integv
import requests
import urllib
from tqdm import tqdm

from libs.path import Path


class Downloader:
    @staticmethod
    def download(url, dest=None, retries=4, **kwargs):
        if dest is None:
            dest = Downloader.create_dest(url)
                
        temp_dest = dest.with_suffix(dest.suffix + ".part")
        
        progress = tqdm(
            desc=f"Downloading {dest.name}", 
            initial=temp_dest.size(), 
            unit="B", 
            unit_scale=True, 
            leave=False,
            unit_divisor=1024, 
            dynamic_ncols=True, 
            bar_format='{l_bar}{bar}| {n_fmt}B/{total_fmt}B [{elapsed}<{remaining}, ' '{rate_fmt}{postfix}]'
            )
        
        with progress:
            for i in range(retries + 1):
                try:
                    Downloader._download(url, temp_dest, progress, **kwargs)
                    break
                except requests.exceptions.RequestException:
                    if i == retries:
                        raise requests.exceptions.RequestException
                    else:
                        progress.set_description(f"Downloading {dest.name} (retry {i+1}/{retries}")
                                                 
        progress.clear()
        
        if Downloader.check_content(temp_dest):
            temp_dest.rename(dest)

    @staticmethod
    def _download(url, dest, progress, headers={}, chunck_size=None, timeout=10, session=None, callback=None, **kwargs):
        if session is None:
            session = requests
            
        if chunck_size is None:
            chunck_size = 32 * 2 ** 10 # 32 KB
        
        headers["Range"] = f"bytes={dest.size()}-"
        stream = session.get(url, headers=headers, timeout=timeout, stream=True)
        
        if stream.status_code == 416: # range not supported
            headers.pop("Range")
            stream = session.get(url, headers=headers, timeout=timeout, stream=True)
            download_size = int(stream.headers["Content-Length"])
            start, end = 0, download_size - 1
        elif "Content-Range" in stream.headers:
            content_range = stream.headers["Content-Range"].split(" ")[1]
            start_end, download_size = content_range.split("/")
            start, end = start_end.split("-")
            start, end, download_size = int(start), int(end), int(download_size)
        else:
            raise requests.exceptions.RequestException
        
        if progress.total is None:
            progress.total = download_size
            
        if dest.size() > start:
            progress.update(-dest.size())
            if callback:
                callback(-dest.size() / progress.total)
            dest.write_bytes(b"") # reset content
        
        with open(dest, "ab") as fp:
            for chunck in stream.iter_content(chunck_size):
                fp.write(chunck)
                progress.update(len(chunck))
                if callback:
                    callback(len(chunck) / progress.total)

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
