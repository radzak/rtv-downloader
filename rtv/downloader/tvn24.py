import datetime
import re

import requests
from bs4 import BeautifulSoup

from rtv.downloader.common import Downloader


class Tvn24DL(Downloader):
    _VALID_URL = r'https?://(?:www\..*)?tvn24\.pl/.*'

    def get_podcast_date(self):
        soup = BeautifulSoup(self.html, 'html.parser')

        div = soup.find('div', class_='articleDateContainer')
        date_str = div.find('time', datetime=True)['datetime']
        podcast_date = datetime.datetime.strptime(date_str, '%Y-%m-%d %H:%M:%S')
        return podcast_date

    # def get_podcast_show_name(self):
    #     title_raw = super().get_info().get('title')
    #     match = re.match(
    #         r'^.*?-\s*(?P<show_name>[\w#\-.,\s]+?)(?=\s*-\s*\d{2}[:.]\d{2}[:.]\d{4}|$)', title_raw)
    #
    #     if match:
    #         return match.group('show_name').replace('-', ' ')

    def get_info(self):
        self.get_html()

        podcast_info = super().get_info()
        self.update_podcast_info_entries(podcast_info, {
            'title': podcast_info.pop('title'),
            # 'show_name': self.get_podcast_show_name(),
            'formats': podcast_info.pop('formats'),
            'description': podcast_info.pop('description'),
            'date': self.get_podcast_date(),
        })
        return podcast_info
