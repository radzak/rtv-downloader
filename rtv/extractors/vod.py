import datetime
import re

from bs4 import BeautifulSoup

from rtv.extractors.common import Extractor


class Vod(Extractor):
    SITE_NAME = 'vod.pl'
    _VALID_URL = r'https?://(?:www\.)?vod\.pl/'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.load_html()
        self.soup = BeautifulSoup(self.html, 'lxml')
        self.headline_match = self._extract_headline()

    def get_date(self):
        # TODO: use better date regex / use dateparser package?
        # "uploadDate": "2018-02-08 12:14:22+0100"
        match = re.search(
            r'\"uploadDate\"'
            r'\s*:\s*' 
            r'\"(?P<date>\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}\+\d{4})\"'
            r'.*',
            self.html)

        if match:
            date_str = match.group('date')
            return datetime.datetime.strptime(date_str, '%Y-%m-%d %H:%M:%S%z')

    def _extract_headline(self):
        div = self.soup.find('div', class_='v_videoTitle')

        if div:
            headline = div.find('h2').find(text=True).strip()

            pattern = re.compile(
                r'^(?:(?P<show_name>[\w#\-.,\s]+?)\.?:\s*)?'  # optional show name
                r'(?P<title>\b[\w#\-.,\s]+\b)'
                r'.*$'
            )
            return pattern.match(headline)

        return None

    def get_show_name(self):
        match = self.headline_match
        if match:
            return match.group('show_name')

    def get_title(self):
        match = self.headline_match
        if match:
            return match.group('title')

    def extract(self):
        entries = [{
            'title': self.get_title(),
            'show_name': self.get_show_name(),
            'date': self.get_date(),
            'url': self.url,
            'ext': 'mp4',
        }]

        return entries
