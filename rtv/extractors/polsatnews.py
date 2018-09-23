import datetime
import re
from typing import Dict

import js2py
from bs4 import BeautifulSoup
from dateparser.search import search_dates

from rtv.extractors.common import Extractor, GenericDescriptionMixin


class PolsatNews(GenericDescriptionMixin, Extractor):
    SITE_NAME = 'polsatnews.pl'
    _VALID_URL = r'https?://(?:www\.)?polsatnews\.pl/'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.load_html()
        self.soup = BeautifulSoup(self.html, 'lxml')
        self.data = self._extract_data()

    def _extract_data(self) -> Dict[str, str]:
        pattern = re.compile(r'(?P<data>customPackage\s*=\s*\[.*?\])', re.DOTALL)
        match = pattern.search(self.html)

        if match:
            data_raw = match.group('data')
            data_list = js2py.eval_js(data_raw)
            data_dict = {d['name'].lower(): d['value'] for d in data_list}
            return data_dict
        return {}

    def get_show_name(self):
        show_name = self.data.get('series')
        return show_name

    def get_title(self):
        title = self.data.get('title')
        return title

    def get_date(self):
        # TODO: refactor, handle if parsing fails, come up with a more generic solution
        div = self.soup.select_one('div.article-meta-data div.fl-right')
        if div:
            date_str = div.text
            date = datetime.datetime.strptime(date_str, '%Y-%m-%d, %H:%M')
            return date

        description = self.get_description()
        found_dates = search_dates(description, languages=['pl'])
        if found_dates:
            _, date = found_dates[0]
            return date

        return None

    def extract(self):
        entries = [{
            'title': self.get_title(),
            'description': self.get_description(),
            'show_name': self.get_show_name(),
            'date': self.get_date(),
            'url': self.url,
            'ext': 'mp4'
        }]

        return entries
