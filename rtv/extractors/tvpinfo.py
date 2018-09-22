import re
from urllib.parse import urlparse

import dateparser
import requests
from bs4 import BeautifulSoup

from rtv.exceptions import VideoIdNotMatchedError
from rtv.extractors.common import Extractor


class TvpInfo(Extractor):
    SITE_NAME = 'tvp.info'
    _VALID_URL = r'https?://(?:www\.)?tvp\.info/'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.url = self.get_article_url()

        # some data will be scraped from the article page
        self.load_html()
        self.soup = BeautifulSoup(self.html, 'lxml')

        # and some data will be scraped from the player page
        self.video_id = self._extract_id()
        self.player_url = self.get_player_url()
        self.player_html = requests.get(self.player_url).text
        self.player_soup = BeautifulSoup(self.player_html, 'lxml')

    def _extract_id(self):
        pattern = re.compile(r'object_id=(?P<id>\d+)')
        match = pattern.search(self.html)

        if match:
            return match.group('id')
        else:
            raise VideoIdNotMatchedError

    def get_article_url(self):
        """
        Get the url of the TVP Info article itself, not the url of the preview with
        the 'Przejdź do artykułu' hyperlink.

        Returns:
            (str): Url of the article with the video.

        """
        html = requests.get(self.url).text
        soup = BeautifulSoup(html, 'lxml')
        div = soup.find('div', class_='more-back')

        if div:
            parsed_uri = urlparse(self.url)
            domain = '{uri.scheme}://{uri.netloc}'.format(uri=parsed_uri)
            suffix = div.find('a', href=True)['href'].strip()
            article_url = domain + suffix
            return article_url
        else:
            return self.url

    def get_player_url(self):
        """
        Get the url of the page containing embedded video player. The html of that page contains
        more detailed data about the video than the article page.
        """
        return f'http://www.tvp.info/sess/tvplayer.php?object_id={self.video_id}'

    def get_date(self):
        span = self.soup.find('span', class_='date')

        if span:
            date_str = span.text
            return dateparser.parse(date_str)

    def get_title(self):
        title = self.player_soup.find('meta', {'property': 'og:title'})['content']
        return title

    def get_showname(self):
        pattern = re.compile(
            r'\"SeriesTitle\",'
            r'\s*value:\s*'
            r'\"(?P<showname>.*?)\"'
        )
        match = pattern.search(self.player_html)

        if match:
            showname = match.group('showname')
            return showname or None

    def get_description(self):
        description = self.player_soup.find('meta', {'property': 'og:description'})['content']
        return description

    def extract(self):
        entries = [{
            'title': self.get_title(),
            'showname': self.get_showname(),
            'description:': self.get_description(),
            'date': self.get_date(),
            'url': self.url,
            'ext': 'mp4',
        }]

        return entries
