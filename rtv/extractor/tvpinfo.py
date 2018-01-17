from urllib.parse import urlparse

import dateparser
import requests
from bs4 import BeautifulSoup

from rtv.extractor.common import Extractor


class TvpInfoDL(Extractor):
    _VALID_URL = r'https?://(?:www\.)?tvp\.info/'

    def get_podcast_date(self):
        real_url = self.get_real_url()
        html = requests.get(real_url).text

        soup = BeautifulSoup(html, 'html.parser')
        span = soup.find('span', class_='date')
        if span:
            date_str = span.text
            return dateparser.parse(date_str)
        else:
            return None

    def get_real_url(self):
        soup = BeautifulSoup(self.html, 'html.parser')
        div = soup.find('div', class_='more-back')
        if div:
            parsed_uri = urlparse(self.url)
            domain = '{uri.scheme}://{uri.netloc}'.format(uri=parsed_uri)
            suffix = div.find('a', href=True)['href'].strip()
            real_url = domain + suffix
            return real_url
        else:
            return self.url

    def get_info(self):
        self.get_html()
        # data = super().get_info()
        # TODO: get rid of super().get_info() call -> instead scrape title, showname and url from
        # 'http://www.tvp.pl/sess/tvplayer.php?object_id={id}'.format(id=object_id)
        # 'https://github.com/rg3/youtube-dl/blob/master/youtube_dl/extractor/tvp.py'

        podcast_info = {
            'entries': [{
                'title': 'xD',
                'description:': 'xD',
                'date': self.get_podcast_date(),
                'url': self.url,
                'ext': 'mp4',
            }]
        }
        return podcast_info
