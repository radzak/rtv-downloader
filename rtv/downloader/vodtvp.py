import datetime
import re

from rtv.downloader.common import Downloader


class VodTVPDL(Downloader):
    _VALID_URL = r'https?://(?:www\.)?vod.tvp\.pl/.*/(?P<show_name>[\w-]+),(?:[\w-]+-)?(?P<date>\d{8}).*'

    def get_podcast_date(self):
        match = re.match(self._VALID_URL, self.url)

        if match:
            date_str = match.group('date')
            return datetime.datetime.strptime(date_str, '%d%m%Y')

    def get_show_name(self):
        show_name_raw = super().get_info().get('title')
        match = re.match(r'(?P<show_name>.*),(?:.*,)?\s*\d{2}.\d{2}.\d{4}', show_name_raw)

        if match:
            return match.group('show_name')

    # TODO: FIX invoking super().get_info() two times, add it as instance attribute and set in init?
    def get_title(self):
        return self.get_show_name()  # These shows have no title, only show_name and description

    # TODO: Scrape title from url and capitalize letters (or from webpage)

    def get_info(self):
        entry = {
            'title': self.get_title(),
            'show_name': self.get_show_name(),
            'date': self.get_podcast_date(),
            'url': self.url,
            'ext': 'mp4'
        }
        return {'entries': [entry]}
