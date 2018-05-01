import datetime
from collections import namedtuple
import json
import re

import requests
from bs4 import BeautifulSoup

from rtv.extractors.common import Extractor
from rtv.exceptions import VideoIdNotMatchedError


class TokFm(Extractor):
    SITE_NAME = 'tokfm.pl'
    _VALID_URL = r'https?://(?:www\.)?audycje\.tokfm\.pl/.*/(?P<video_id>[a-z0-9-]*)'
    VideoInfo = namedtuple('VideoInfo', ('date', 'showname', 'host', 'guests'))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.get_html()
        self.soup = BeautifulSoup(self.html, 'html.parser')
        self.video_id = self._extract_id()
        self.info = self._scrape_info()

    def get_real_url(self):
        data = {'pid': self.video_id, 'st': 'tokfm'}
        r = requests.post('http://audycje.tokfm.pl/gets', data=json.dumps(data), cookies=self.request.cookies)
        url = json.loads(r.text)['url']
        return url

    def _extract_id(self):
        """
        Get video_id needed to obtain real_url of the video.

        Returns:
            re.match object

        Raises:
            VideoIdNotMatchedError: If video_id is not matched with regular expression.

        """
        match = re.match(self._VALID_URL, self.url)

        if match:
            return match.group('video_id')
        else:
            raise VideoIdNotMatchedError

    def _process_info(self, raw_info: VideoInfo) -> VideoInfo:
        """Process raw information about the video (parse date, etc.)."""
        raw_date = raw_info.date
        date = datetime.datetime.strptime(raw_date, '%Y-%m-%d %H:%M')  # 2018-04-05 17:00
        video_info = raw_info._replace(date=date)
        return video_info

    def _scrape_info(self) -> VideoInfo:
        rows = self.soup.select('.tok-divTableRow')[:-2]  # omit duration SocialMedia links
        cells = [row.select('.tok-divTableCell')[1] for row in rows]
        cells[1].find('span').decompose()  # delete "Obserwuj" text

        data = [cell.get_text(strip=True) for cell in cells]
        raw_info = self.VideoInfo(*data)
        video_info = self._process_info(raw_info)
        return video_info

    def get_title(self):
        title = self.soup.select_one('meta[property="og:title"]')['content']
        return title

    def get_description(self):
        title = self.soup.select_one('meta[property="og:description"]')['content']
        return title

    def extract(self):
        entries = [{
            **self.info._asdict(),
            'title': self.get_title(),
            'description': self.get_description(),
            'url': self.get_real_url(),
            'ext': 'mp3'
        }]

        return entries
