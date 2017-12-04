import datetime
import re

from bs4 import BeautifulSoup

from rtv.downloader.common import Downloader


class RadioZetDL(Downloader):
    _VALID_URL = r'https?://(?:www\.)?radiozet\.pl/.*/(?P<show_name>[\w\-.,]+)/(?P<title>[\w\-.,]+)'

    def get_real_url(self):
        soup = BeautifulSoup(self.html, 'html.parser')

        # manifests available:
        # data-source-ss
        # data-source-dash
        # data-source-hls
        manifest_url = [item['data-source-dash'] for item in soup.find_all()
                        if 'data-source-dash' in item.attrs][0]
        return manifest_url

    def get_podcast_date(self):
        soup = BeautifulSoup(self.html, 'html.parser')

        date_str = [item['data-date'] for item in soup.find_all() if 'data-date' in item.attrs][0]
        podcast_date = datetime.datetime.strptime(date_str, '%d.%m.%Y %H:%M')
        return podcast_date

    def get_podcast_title(self):
        # TODO: scrape title from web
        match = re.match(self._VALID_URL, self.url)
        return match.group('title').replace('-', ' ')

    def get_podcast_show_name(self):
        # TODO: scrape show_name from web
        match = re.match(self._VALID_URL, self.url)
        return match.group('show_name').replace('-', ' ')

    def get_info(self):
        self.get_html()

        podcast_info = {}
        self.update_podcast_info_entries(podcast_info, {
            'url': self.get_real_url(),
            'title': self.get_podcast_title(),
            'show_name': self.get_podcast_show_name(),
            'date': self.get_podcast_date(),
            'ext': 'mp4'
        })
        return podcast_info
