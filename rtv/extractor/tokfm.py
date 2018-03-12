import datetime
import json
import re

import requests
from bs4 import BeautifulSoup

from rtv.extractor.common import Extractor
from rtv.exceptions import PodcastIdNotMatchedError


class TokFm(Extractor):
    SITE_NAME = 'tokfm.pl'
    _VALID_URL = r'https?://(?:www\.)?audycje\.tokfm\.pl/.*/(?P<podcast_id>[a-z0-9-]*)'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.get_html()
        self.soup = BeautifulSoup(self.html, 'html.parser')
        self.podcast_id = self._extract_id()

    def get_real_url(self):
        data = {'pid': self.podcast_id, 'st': 'tokfm'}
        r = requests.post('http://audycje.tokfm.pl/gets', data=json.dumps(data))
        url = json.loads(r.text)['url']
        return url

    def _extract_id(self):
        """
        Get podcast_id needed to obtain real_url of the podcast.

        Returns:
            re.match object

        Raises:
            PodcastIdNotMatchedError: If podcast_id is not matched with regular expression.

        """
        match = re.match(self._VALID_URL, self.url)

        if match:
            return match.group('podcast_id')
        else:
            raise PodcastIdNotMatchedError

    @staticmethod
    def _parse_podcast_date(date_str):
        date = datetime.datetime.strptime(date_str, '%d-%m-%Y')
        return date

    def scrape_podcast_info(self):
        # scrape date, show_name, guests and tags
        tables = self.soup.findChildren('table')
        podcast_table = tables[0]  # TODO: locate it better

        info = {}
        for row in podcast_table.findAll('tr'):
            aux = row.findAll('td')
            info[aux[0].string] = aux[1].text

        # scrape title
        article = self.soup.find('article', class_='tytul-odcinka')
        info['Tytuł:'] = article.find('h1').text

        # translate dict key names
        info = {
            'date': self._parse_podcast_date(info.get('Data emisji:')),
            'title': info.get('Tytuł:'),
            'show_name': info.get('Audycja:'),
            'hosts': info.get('Prowadzący:'),
            'guests': info.get('Goście:'),
            'tags': info.get('Tagi:')
        }

        return info

    def extract(self):
        entries = [{
            **self.scrape_podcast_info(),  # title, show_name, date, etc.
            'url': self.get_real_url(),
            'ext': 'mp3'
        }]

        return entries
