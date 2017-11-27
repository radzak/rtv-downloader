import datetime
import re
import requests

from rtv.downloader.common import Downloader
from rtv.utils import TitleNotMatchedError, DateNotMatchedError


class VodDL(Downloader):
    _VALID_URL = r'https?://(?:www\.)?vod\.pl/'

    @classmethod
    def get_podcast_date(cls, url):
        r = requests.get(url)
        html = r.text

        match = re.search(r'\'datePublished\'\s+:\s+\'(?P<date>\d{4}-\d{2}-\d{2}).*', html)

        if match:
            date_str = match.group('date')
        else:
            raise DateNotMatchedError

        podcast_date = datetime.datetime.strptime(date_str, '%Y-%m-%d')
        return podcast_date

    @classmethod
    def get_show_name(cls, url):
        show_name_raw = super().get_info(url).get('title')
        match = re.match(r'^(?P<show_name>[\w#\-.,\s]+):.*$', show_name_raw)

        if match:
            return match.group('show_name')
        else:
            raise TitleNotMatchedError

    @classmethod
    def get_title(cls, url):
        title_raw = super().get_info(url).get('title')
        match = re.match(r'^.*:\s*(?P<title>\b[\w#\-.,\s]+\b)\s*(?:\(\d{2}[:.]\d{2}\))?$', title_raw)

        if match:
            return match.group('title')
        else:
            raise TitleNotMatchedError

    @classmethod
    def get_info(cls, url):
        podcast_info = super().get_info(url)
        podcast_info.update({
            'title': cls.get_title(url),
            'show_name': cls.get_show_name(url),
            'date': cls.get_podcast_date(url),
        })
        return podcast_info
