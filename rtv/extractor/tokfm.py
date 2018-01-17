import datetime
import json
import re

import requests
from bs4 import BeautifulSoup

from rtv.extractor.common import Extractor
from rtv.exceptions import PodcastIdNotMatchedError


class TokFmDL(Extractor):
    _VALID_URL = r'https?://(?:www\.)?audycje\.tokfm\.pl/.*/(?P<podcast_id>[a-z0-9-]*)'

    def get_real_url(self):
        podcast_id = self.get_podcast_id()
        data = {'pid': podcast_id, 'st': 'tokfm'}
        r = requests.post('http://audycje.tokfm.pl/gets', data=json.dumps(data))
        url = json.loads(r.text)['url']
        return url

    def get_podcast_id(self):
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
        self.get_html()
        soup = BeautifulSoup(self.html, 'html.parser')

        # scrape date, show_name, guests and tags
        tables = soup.findChildren('table')
        podcast_table = tables[0]  # TODO: locate it better

        info = {}
        for row in podcast_table.findAll('tr'):
            aux = row.findAll('td')
            info[aux[0].string] = aux[1].text

        # scrape title
        article = soup.find('article', class_='tytul-odcinka')
        info['Tytuł:'] = article.find('h1').text

        # translate dict key names
        info = {
            'date': self._parse_podcast_date(info.get('Data emisji:')),
            'hosts': info.get('Prowadzący:'),
            'guests': info.get('Goście:'),
            'show_name': info.get('Audycja:'),
            'tags': info.get('Tagi:'),
            'title': info.get('Tytuł:')
        }

        return info

    def get_info(self):
        podcast_info = {
            'entries': [{
                **self.scrape_podcast_info(),  # title, show_name, date, etc.
                'url': self.get_real_url(),
                'ext': 'mp3'
            }]
        }
        return podcast_info
