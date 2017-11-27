from bs4 import BeautifulSoup
import datetime
import requests

from rtv.downloader.common import Downloader


class RadioZetDL(Downloader):
    _VALID_URL = r'https?://(?:www\.)?radiozet\.pl/.*/(?P<show_name>[\w-]+)/(?P<title>[\w-]+)'

    @classmethod
    def get_real_url(cls, url):
        r = requests.get(url)
        html = r.text

        soup = BeautifulSoup(html, 'html.parser')

        # manifests available:
        # data-source-ss
        # data-source-dash
        # data-source-hls
        manifest_url = [item['data-source-dash'] for item in soup.find_all() if 'data-source-dash' in item.attrs][0]
        return manifest_url

    @classmethod
    def get_podcast_date(cls, url):
        r = requests.get(url)
        html = r.text

        soup = BeautifulSoup(html, 'html.parser')

        date_str = [item['data-date'] for item in soup.find_all() if 'data-date' in item.attrs][0]
        podcast_date = datetime.datetime.strptime(date_str, '%d.%m.%Y %H:%M')
        return podcast_date

    @classmethod
    def get_info(cls, url):
        podcast_info = super().get_info(url)
        podcast_info.update(
            {'title': cls.validate_url(url).group('title'),  # TODO: check if not better to scrape url
             'show_name': cls.validate_url(url).group('show_name'),
             'date': cls.get_podcast_date(url),
             'ext': 'mp4'
             })
        return podcast_info
