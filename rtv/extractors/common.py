import re
from typing import Any, ClassVar, Dict, List, Match, Optional

import requests
import youtube_dl
from bs4 import BeautifulSoup

from rtv.utils import get_domain_name, suppress_stdout
from rtv.video import Video

Entry = Dict[str, Any]
Entries = List[Entry]


class Extractor:
    SITE_NAME: ClassVar[str]
    _VALID_URL: ClassVar[str]

    url: str
    html: str
    videos: List[Video]
    response: requests.models.Response

    def __init__(self, url: str) -> None:
        self.url = url
        self.videos = []

    @classmethod
    def validate_url(cls, url: str) -> Optional[Match[str]]:
        """Check if the Extractor can handle the given url."""
        match = re.match(cls._VALID_URL, url)
        return match

    def load_html(self) -> None:
        r = requests.get(self.url)
        r.encoding = 'utf-8'
        self.response = r
        self.html = r.text

    def get_info(self) -> dict:
        """Get information about the videos from YoutubeDL package."""
        with suppress_stdout():
            with youtube_dl.YoutubeDL() as ydl:
                info_dict = ydl.extract_info(self.url, download=False)
                return info_dict

    @staticmethod
    def update_entries(entries: Entries, data: dict) -> None:
        """Update each entry in the list with some data."""
        # TODO: Is mutating the list okay, making copies is such a pain in the ass
        for entry in entries:
            entry.update(data)

    def extract(self) -> Entries:
        """Extract data from the url. Redefine in subclasses."""
        raise NotImplementedError('This method must be implemented by subclasses')

    def run(self) -> None:
        entries = self.extract()

        self.update_entries(entries, {
            'site': get_domain_name(self.url)
        })

        if not isinstance(entries, list):
            raise TypeError('extract method must return an iterable of dictionaries')

        for entry in entries:
            video = Video(entry)
            self.videos.append(video)


class GenericTitleMixin:
    soup: BeautifulSoup

    def get_title(self) -> Optional[str]:
        meta_tag = self.soup.select_one('meta[property="og:title"]')
        if meta_tag:
            title = meta_tag.get('content')
            return title
        return None


class GenericDescriptionMixin:
    soup: BeautifulSoup

    def get_description(self) -> Optional[str]:
        meta_tag = self.soup.select_one('meta[property="og:description"]')
        if meta_tag:
            description = meta_tag.get('content')
            return description
        return None
