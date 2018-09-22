import datetime
import re

import js2py
import requests
from bs4 import BeautifulSoup

from rtv.extractors.common import Extractor


class TvpParlament(Extractor):
    SITE_NAME = 'tvpparlament.pl'
    _VALID_URL = r'https?://(?:www\.)?tvpparlament\.pl/'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.load_html()
        self.soup = BeautifulSoup(self.html, 'lxml')
        self.data = self._fetch_data()

    @staticmethod
    def _get_json_url(*, object_id, sdt_version, **kwargs):
        json_url = (
            f'http://www.tvpparlament.pl/shared/cdn/tokenizer_v2.php'
            f'?object_id={object_id}'
            f'&std_version={sdt_version}'
        )
        return json_url

    def _fetch_data(self):
        pattern = re.compile(r'(?P<video_ids>playVideo\s*=\s*{.*})', re.DOTALL)
        script = self.soup.find('script', text=pattern)
        match = pattern.search(script.text)

        video_ids_raw = match.group('video_ids')
        video_ids = js2py.eval_js(f'Object({video_ids_raw})').to_dict()

        json_url = self._get_json_url(**video_ids)
        video_data = requests.get(json_url).json()

        return video_data

    def get_date(self):
        pattern = re.compile(r'[dD]ata:?\s+(?P<date>\d{2,4}-\d{1,2}-\d{1,2})')
        div = self.soup.find('div', text=pattern)
        match = pattern.search(div.text)

        date_str = match.group('date')
        date = datetime.datetime.strptime(date_str, '%Y-%m-%d')

        return date

    def get_show_name(self):
        # TODO: scrape show_name from web
        pattern = re.compile(r'https?://(?:www\.)?tvpparlament\.pl/(?P<show_name>[\w\-.,]+)/')
        match = pattern.match(self.url)
        return match.group('show_name').replace('-', ' ').title()

    def extract(self):
        # choose format providing manifest as it gives much flexibility in terms of quality choice
        entry = next((item for item in self.data['formats']
                      if item['mimeType'] == 'application/vnd.ms-ss'), None)

        entries = [{
            'title': self.data.get('title'),
            'show_name': self.get_show_name(),
            'date': self.get_date(),
            'url': entry['url'],
            'ext': 'mp4',
        }]

        return entries
