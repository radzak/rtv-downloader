import datetime
import os
import re
import time
import uuid
from youtube_dl import YoutubeDL

from rtv.utils import run_command, clean_filename


class PathNotMatchedError(Exception):
    pass


class Downloader:
    _VALID_URL = None  # Redefine in subclasses.

    @classmethod
    def validate_url(cls, url):
        """ Check if the Downloader can handle the specific url."""
        match = re.match(cls._VALID_URL, url)
        return match

    @classmethod
    def get_real_url(cls, url):
        """ Get the real url of video/audio file."""
        return url

    @classmethod
    def _real_download(cls, path, url):
        """ Redefine in subclasses."""
        run_command(f'youtube-dl -f worst[ext=mp4]/worstvideo+bestaudio/bestaudio '
                    f'--merge-output-format "mp4" '
                    f'-o "{path}" '
                    f'{url}')
        # TODO: add quality/format? option handling
        # TODO: fixed mp4 format - improve it

    @classmethod
    def download_podcast(cls, url, dl_path, name_tmpl):
        real_url = cls.get_real_url(url)

        unique_filename = str(uuid.uuid4())
        extension = cls.get_info(url).get('ext')
        tmp_path = os.path.join(dl_path, f'{unique_filename}.{extension}')

        cls._real_download(tmp_path, real_url)

        new_path = cls.generate_path(tmp_path, dl_path, name_tmpl, url)
        cls.rename_podcast(tmp_path, new_path)

    @classmethod
    def get_info(cls, url):
        # TODO: supress output in this block?
        with YoutubeDL() as ydl:
            info_dict = ydl.extract_info(url, download=False)
            return info_dict

    @classmethod
    def generate_path(cls, current_path, dl_path, name_tmpl, url):
        path_tmpl = os.path.join(dl_path, name_tmpl)

        metadata = cls.get_metadata(current_path)
        info = cls.get_info(url)
        file_info = {**metadata, **info}

        path = cls.render_path(path_tmpl, file_info)
        return path

    @classmethod
    def get_metadata(cls, path):
        metadata = dict()
        metadata['date'] = datetime.datetime.strptime(time.ctime(os.path.getmtime(path)), "%a %b %d %H:%M:%S %Y")
        metadata['size'] = os.path.getsize(path)
        return metadata

    @classmethod
    def render_path(cls, path_tmpl, file_info):
        path = path_tmpl.format(
            date=file_info['date'],
            show_name=file_info.get('show_name', 'default show_name'),
            title=file_info.get('title', 'default title'),
            ext=file_info.get('ext', 'abc')  # add reasonable default
        )
        # TODO: clean, preprocessing of the values in file_info that gonna be used and just unpack file_info dict

        location, filename = os.path.split(path)
        filename = clean_filename(filename)
        path = os.path.join(location, filename)

        return path

    @classmethod
    def rename_podcast(cls, old_path, new_path):
        os.rename(old_path, new_path)
