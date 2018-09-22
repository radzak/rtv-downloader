from datetime import datetime
from typing import List, Optional, Tuple

import dateparser
import requests
from bs4 import BeautifulSoup

from rtv.extractors.common import Entries, Extractor


class Wp(Extractor):
    SITE_NAME = 'wp.pl'
    _VALID_URL = r'https?://(?:www\.)?video\.wp\.pl/.*'

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.load_html()
        self.soup = BeautifulSoup(self.html, 'lxml')
        self.data = self._fetch_data()

    @staticmethod
    def _get_json_url(mid: int) -> str:
        json_url = f'https://video.wp.pl/api/v1/embed/{mid}'
        return json_url

    def _fetch_data(self):
        mid = self.soup.select_one('#mainPlayer')['data-mid']
        json_url = self._get_json_url(mid)
        video_data = requests.get(json_url).json()['clip']
        return video_data

    def get_title(self) -> Optional[str]:
        title = self.data.get('title')
        return title

    def get_description(self) -> Optional[str]:
        description = self.data.get('description')
        return description

    def get_tags(self) -> List[str]:
        tags = self.data.get('tags', '').split(',')
        return tags

    def get_show_name(self) -> Optional[str]:
        show_name = self.data['media'].get('program')
        return show_name

    def get_date(self) -> Optional[datetime]:
        raw_date = self.data['media'].get('createDate')
        if raw_date:
            date = dateparser.parse(raw_date)
            return date
        return None

    @staticmethod
    def quality_comparator(video_data):
        """Custom comparator used to choose the right format based on the resolution."""
        def parse_resolution(res: str) -> Tuple[int, ...]:
            return tuple(map(int, res.split('x')))

        raw_resolution = video_data['resolution']
        resolution = parse_resolution(raw_resolution)
        return resolution  # e.g (1024, 576)

    def get_real_url(self) -> str:
        formats = list(filter(lambda d: d['type'] == 'mp4@avc', self.data['url']))  # filter out mp4
        worst_format = min(formats, key=self.quality_comparator)  # for now take the lowest quality
        url = worst_format['url']
        return url

    def extract(self) -> Entries:
        entries = [{
            'title': self.get_title(),
            'description': self.get_description(),
            'tags': self.get_tags(),
            'show_name': self.get_show_name(),
            'date': self.get_date(),
            'url': self.get_real_url(),
            'ext': 'mp4'
        }]
        return entries
