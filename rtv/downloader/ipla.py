from bs4 import BeautifulSoup
import datetime
import json
import requests
import urllib.request

from rtv.downloader.common import Downloader
from rtv.utils import get_ext


class IplaDL(Downloader):
    _VALID_URL = r'https?://(?:www\.)?ipla\.tv/'

    @classmethod
    def _parse_podcast_date(cls, date_raw):
        data = datetime.datetime.strptime(date_raw, '%d-%m-%Y')
        return data

    @classmethod
    def get_json_url(cls, url):
        r = requests.get(url)
        html = r.text
        soup = BeautifulSoup(html, 'html.parser')
        data_vod = soup.find('div', {'id': 'vod-player'})['data-vod-json']
        data_vod_json = json.loads(data_vod)

        url = 'http://getmedia.redefine.pl/vods/get_vod/?cpid={cpid}&ua=mipla_ios/122&media_id={mid}'.format(
            **data_vod_json
        )
        return url

    @classmethod
    def get_real_url(cls, url):
        """
        Temporary solution for getting url of the worstpossible quality.
        It will get enhanced as soon as we introduce the quality choice option.
        """
        # TODO: introduce quality choice option
        podcast_info = cls.get_info(url)

        formats = podcast_info['copies']
        url = min(formats, key=lambda k: k['quality'])['url']  # temporary solution, just get the lowest quality
        return url

    @classmethod
    def get_info(cls, url):
        url = cls.get_json_url(url)
        r = requests.get(url)
        podcast_info = r.json()['vod']
        podcast_info.update({
            'date': cls._parse_podcast_date(podcast_info['date']),
            'ext': get_ext(podcast_info['video_hd']),
        })
        print(podcast_info['title'])
        return podcast_info

    @classmethod
    def _real_download(cls, path, url):
        # https://stackoverflow.com/questions/2795331/python-download-without-supplying-a-filename
        urllib.request.urlretrieve(url, f'{path}')
