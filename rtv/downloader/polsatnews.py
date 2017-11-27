from bs4 import BeautifulSoup
import datetime
import re
import requests

from rtv.downloader.common import Downloader
from rtv.utils import TitleNotMatchedError


class PolsatNewsDL(Downloader):
    _VALID_URL = r'https?://(?:www\.)?polsatnews\.pl/.*'

    @classmethod
    def get_podcast_date(cls, url):
        r = requests.get(url)
        html = r.text
        soup = BeautifulSoup(html, 'html.parser')

        date_str = soup.find('div', class_='article-meta-data').find('div', class_='fl-right').text
        podcast_date = datetime.datetime.strptime(date_str, '%Y-%m-%d, %H:%M')
        return podcast_date

    @classmethod
    def get_show_name(cls, url):
        title_raw = super().get_info(url).get('title')  # TODO: add error handling if not found (not only here)
        match = re.match(r'^.*?-\s*(?P<show_name>[\w#\-.,\s]+?)(?=\s*-\s*\d{2}[:.]\d{2}[:.]\d{4}|$)', title_raw)

        if match:
            return match.group('show_name').replace('-', ' ')
        else:
            raise TitleNotMatchedError

    @classmethod
    def get_title(cls, url):
        return cls.get_show_name(url)  # These shows have no title, only show_name and description

    @classmethod
    def get_info(cls, url):
        podcast_info = super().get_info(url)
        podcast_info.update(
            {'title': cls.get_title(url),
             'show_name': cls.get_show_name(url),
             'date': cls.get_podcast_date(url),
             'ext': 'mp4'
             })
        return podcast_info
