import datetime
import json
import re

import requests
from dateparser.search import search_dates
from bs4 import BeautifulSoup

from rtv.exceptions import VideoIdNotMatchedError
from rtv.extractors.common import Extractor
from rtv.utils import get_ext


class Ipla(Extractor):
    SITE_NAME = 'ipla.tv'
    _VALID_URL = r'https?://(?:www\.)?ipla\.tv/.*/(?P<id>[0-9a-fA-F]+)'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.video_id = self._extract_id()
        self.load_html()
        self.soup = BeautifulSoup(self.html, 'lxml')
        self.data = self._fetch_data()

    @staticmethod
    def _generate_client_id(length):
        import binascii
        import os

        return binascii.b2a_hex(os.urandom(length // 2))

    def _extract_id(self):
        # TODO: move to extractor.common? maybe merge with validate_url?
        match = re.search(self._VALID_URL, self.url)

        if match:
            return match.group('id')
        else:
            raise VideoIdNotMatchedError

    def _fetch_data(self):
        url = 'https://b2c.redefine.pl/rpc/navigation/'
        data = {
            'jsonrpc': '2.0',
            'id': 1,
            'method': 'prePlayData',
            'params': {
                'ua': 'www_iplatv_html5/12345',
                # 'ua': 'www_iplatv_html5/12345 (Windows 10; widevin=true)',
                #  can be used to get dash manifest
                'cpid': 1,
                'mediaId': self.video_id
            }
        }

        video_data = requests.post(url, data=json.dumps(data)).json()
        return video_data

    def get_date(self):
        description_tag = self.soup.select_one('.description-content__paragraph')
        description = description_tag.get_text(strip=True)
        found_dates = search_dates(description, languages=['pl'])

        if found_dates:
            _, date = found_dates[0]
        else:
            # TODO: handle if not present
            date_str = self.data['result']['reporting']['gastream']['premiereDate']
            date = datetime.datetime.strptime(date_str, '%Y%m%d')
        return date

    def get_title(self):
        # soup = BeautifulSoup(self.html, 'lxml')
        # title = soup.find('h1', class_='vod-title__content').text
        title = self.data['result']['reporting']['gastream']['title']  # TODO: handle if not present
        return title

    def get_showname(self):
        # TODO: handle if not present
        showname = self.data['result']['reporting']['gastream']['series']
        return showname

    def get_real_url(self):
        sources = self.data['result']['mediaItem']['playback']['mediaSources']
        source = min(sources, key=lambda s: s['quality'][:-1])  # choose lowest quality, e.g. 576p
        # TODO: handle all qualities

        key_id = source['keyId']
        getmedia_url = source['authorizationServices']['pseudo']['url']
        payload = {
            'cpid': 1,
            'id': self.video_id,
            'clid': self._generate_client_id(32),
            'keyid': key_id,
            'ua': 'www_iplatv_html5/12345'
        }

        response = requests.get(getmedia_url, params=payload)
        media_url = response.json()['resp']['license']['url']

        return media_url

    def extract(self):
        # TODO: check why ipla extracting takes so long (~20+ seconds?? for 3 requests??)
        url = self.get_real_url()

        entries = [{
            'title': self.get_title(),
            'showname': self.get_showname(),
            'date': self.get_date(),
            'url': url,
            'ext': get_ext(url),
        }]

        return entries
