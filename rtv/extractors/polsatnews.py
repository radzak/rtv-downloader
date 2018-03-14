import datetime
import re

import js2py
from bs4 import BeautifulSoup

from rtv.extractors.common import Extractor


class PolsatNews(Extractor):
    SITE_NAME = 'polsatnews.pl'
    _VALID_URL = r'https?://(?:www\.)?polsatnews\.pl/'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.get_html()
        self.soup = BeautifulSoup(self.html, 'html.parser')
        self.data = self._extract_data()

    def get_date(self):
        div = self.soup.find('div', class_='article-meta-data').find('div', class_='fl-right')
        date_str = div.text
        date = datetime.datetime.strptime(date_str, '%Y-%m-%d, %H:%M')
        return date

    def _extract_data(self):
        # TODO: add error handling if there is no script with customPackage variable
        pattern = re.compile(r'(?P<data>customPackage\s*=\s*\[.*?\])', re.DOTALL)
        match = pattern.search(self.html)

        data_raw = match.group('data')
        data_list = js2py.eval_js(data_raw)
        data_dict = {d['name'].lower(): d['value'] for d in data_list}

        return data_dict

    def get_show_name(self):
        show_name = self.data.get('series')
        return show_name

    def get_title(self):
        title = self.data.get('title')
        return title

    def extract(self):
        entries = [{
            'title': self.get_title(),
            'show_name': self.get_show_name(),
            'date': self.get_date(),
            'url': self.url,
            'ext': 'mp4'
        }]

        return entries
