import datetime
import js2py
import re

from bs4 import BeautifulSoup

from rtv.extractors.common import Extractor
from rtv.utils import get_ext


class Rmf24(Extractor):
    SITE_NAME = 'rmf24.pl'
    _VALID_URL = r'https?://(?:www\.)?rmf24\.pl/'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.get_html()
        self.soup = BeautifulSoup(self.html, 'html.parser')

    def get_date(self):
        dates = self.soup.find('div', class_='article-date')
        date_published_str = dates.find('meta', {'itemprop': 'datePublished'}).attrs['content']

        try:
            return datetime.datetime.strptime(date_published_str, '%Y-%m-%dT%H:%M:%S')
        except ValueError:
            return None

    def _get_audio_entries(self) -> list:
        # .embed .audio
        entries = [audio['src'] for audio in self.soup.find_all('audio')]
        return entries

    def _get_video_entries(self) -> list:
        # .embed-video video > source
        entries = [video['src'] for video in self.soup.select('video > source')]
        return entries

    def _scrape_entries(self):
        audio_entries = self._get_audio_entries()
        video_entries = self._get_video_entries()

        # temporarily return only audio entries if present, otherwise return all video entries
        if audio_entries:
            entries = audio_entries
        else:
            entries = video_entries

        print(entries)

        return entries

    def extract(self):
        entries = self._scrape_entries()

        self.update_entries(entries, {
            'date': self.get_date(),
        })

        print(entries)
        import sys
        sys.exit(1)

        return entries
