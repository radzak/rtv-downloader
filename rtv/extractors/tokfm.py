import datetime
import json
import re

import requests
from bs4 import BeautifulSoup

from rtv.extractors.common import Extractor
from rtv.exceptions import VideoIdNotMatchedError


class TokFm(Extractor):
    SITE_NAME = 'tokfm.pl'
    _VALID_URL = r'https?://(?:www\.)?audycje\.tokfm\.pl/.*/(?P<video_id>[a-z0-9-]*)'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.get_html()
        self.soup = BeautifulSoup(self.html, 'html.parser')
        self.video_id = self._extract_id()

    def get_real_url(self):
        data = {'pid': self.video_id, 'st': 'tokfm'}
        r = requests.post('http://audycje.tokfm.pl/gets', data=json.dumps(data))
        url = json.loads(r.text)['url']
        return url

    def _extract_id(self):
        """
        Get video_id needed to obtain real_url of the video.

        Returns:
            re.match object

        Raises:
            VideoIdNotMatchedError: If video_id is not matched with regular expression.

        """
        match = re.match(self._VALID_URL, self.url)

        if match:
            return match.group('video_id')
        else:
            raise VideoIdNotMatchedError

    @staticmethod
    def _parse_date(date_str):
        date = datetime.datetime.strptime(date_str, '%d-%m-%Y')
        return date

    def scrape_info(self):
        # scrape date, show_name, guests and tags
        tables = self.soup.findChildren('table')
        video_table = tables[0]  # TODO: locate it better

        info = {}
        for row in video_table.findAll('tr'):
            aux = row.findAll('td')
            info[aux[0].string] = aux[1].text

        # scrape title
        article = self.soup.find('article', class_='tytul-odcinka')
        info['Tytuł:'] = article.find('h1').text

        # translate dict key names
        info = {
            'date': self._parse_date(info.get('Data emisji:')),
            'title': info.get('Tytuł:'),
            'show_name': info.get('Audycja:'),
            'hosts': info.get('Prowadzący:'),
            'guests': info.get('Goście:'),
            'tags': info.get('Tagi:')
        }

        return info

    def extract(self):
        entries = [{
            **self.scrape_info(),  # title, show_name, date, etc.
            'url': self.get_real_url(),
            'ext': 'mp3'
        }]

        return entries
