import datetime
import json

import requests
from bs4 import BeautifulSoup

from rtv.downloader.common import Downloader
from rtv.utils import get_ext


class IplaDL(Downloader):
    _VALID_URL = r'https?://(?:www\.)?ipla\.tv/'

    @staticmethod
    def _parse_podcast_date(date_str):
        date = datetime.datetime.strptime(date_str, '%d-%m-%Y')
        return date

    def get_json_url(self):
        r = requests.get(self.url)
        html = r.text
        soup = BeautifulSoup(html, 'html.parser')
        data_vod = soup.find('div', {'id': 'vod-player'})['data-vod-json']
        data_vod_json = json.loads(data_vod)

        url = 'http://getmedia.redefine.pl/vods/get_vod/?cpid={cpid}&ua=mipla_ios/122&media_id={mid}'.format(
            **data_vod_json
        )
        return url

    def get_info(self):
        """
        Get info about the ipla podcast - get the url containing json data and construct
        a dictionary with 'entries' key.
        Returns:
            dict: Podcast info dictionary.

        """
        url = self.get_json_url()
        r = requests.get(url)
        podcast_info = r.json()['vod']

        # TODO: Refactor & put copies into formats key

        formats = podcast_info['copies']
        entry = min(formats, key=lambda k: k['quality'])  # temporary solution, just get the lowest quality

        podcast_info.update(entry)
        podcast_info.update({
            'description': podcast_info.pop('long_text'),
            'date': self._parse_podcast_date(podcast_info['date']),
            'ext': get_ext(podcast_info['url']),
        })

        del podcast_info['copies']
        return {'entries': [podcast_info]}
