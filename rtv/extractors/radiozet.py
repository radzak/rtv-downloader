import datetime
import re

from bs4 import BeautifulSoup

from rtv.extractors.common import Extractor
from rtv.utils import delete_duplicates


class RadioZet(Extractor):
    SITE_NAME = 'radiozet.pl'
    _VALID_URL = r'https?://(?:www\.)?radiozet\.pl/.*/(?P<show_name>[\w\-.,]+)/(?P<title>[\w\-.,]+)'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.load_html()
        self.soup = BeautifulSoup(self.html, 'lxml')

    def get_entries(self):
        # manifests available:
        # data-source-ss
        # data-source-dash
        # data-source-hls
        divs = delete_duplicates(item for item in self.soup.find_all()
                                 if 'data-source-dash' in item.attrs)

        # sort divs by id, first cast it to int
        # e.g. data-storage-id="90164"
        divs.sort(key=lambda u: int(u['data-storage-id']))

        # extract urls of dash manifests
        manifest_urls = [div['data-source-dash'] for div in divs]

        entries = [{
            'url': url,
            'title': self.get_title(),
            'show_name': self.get_show_name(),
            'date': self.get_date(),
            'ext': 'mp4'
        } for url in manifest_urls]

        # radiozet videos are usually divided into 2 or more videos,
        # a suffix is appended to the title, so there are no duplicated titles
        if len(entries) > 1:
            for index, entry in enumerate(entries, 1):
                entry['title'] += f', part {index}'

        return entries

    def get_date(self):
        date_str = [item['data-date'] for item in self.soup.find_all() if 'data-date' in item.attrs][0]
        # refactor
        date = datetime.datetime.strptime(date_str, '%d.%m.%Y %H:%M')
        return date

    def get_title(self):
        # TODO: scrape title from web?
        match = re.match(self._VALID_URL, self.url)
        return match.group('title').replace('-', ' ')

    def get_show_name(self):
        # TODO: scrape show_name from web?
        match = re.match(self._VALID_URL, self.url)
        return match.group('show_name').replace('-', ' ')

    def extract(self):
        return self.get_entries()
