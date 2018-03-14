import re

import requests
import youtube_dl

from rtv.video import Video
from rtv.utils import suppress_stdout, get_domain_name


class Extractor:
    SITE_NAME = None
    _VALID_URL = None

    def __init__(self, url):
        self.url = url
        self.html = None
        self.videos = []

    @classmethod
    def validate_url(cls, url):
        """
        Check if the Extractor can handle the given url.

        Args:
            url (str): Url of the video.

        Returns:
            re.match object or None if the string does not match the pattern.

        """
        match = re.match(cls._VALID_URL, url)
        return match

    def get_html(self):
        r = requests.get(self.url)
        r.encoding = 'utf-8'
        self.html = r.text

    def get_info(self):
        """
        Get information about the videos from YoutubeDL package.

        Returns:
            dict: Dictionary containing various information such as title, extension, date.

        """
        with suppress_stdout():
            with youtube_dl.YoutubeDL() as ydl:
                info_dict = ydl.extract_info(self.url, download=False)
                return info_dict

    @staticmethod
    def update_entries(entries: list, data: dict):
        """Update each entry in the list with some data."""
        # TODO: Is mutating the list okey, making copies is such a pain in the ass
        for entry in entries:
            entry.update(data)

    def extract(self):
        """Extract data from the url. Redefine in subclasses."""
        raise NotImplementedError('This method must be implemented by subclasses')

    def run(self):
        entries = self.extract()

        self.update_entries(entries, {
            'site': get_domain_name(self.url)
        })

        if not isinstance(entries, list):
            raise TypeError('extract method must return an iterable of dictionaries')

        for entry in entries:
            video = Video(entry)
            self.videos.append(video)
