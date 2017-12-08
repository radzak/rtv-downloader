import datetime
import js2py
import re
import requests

from bs4 import BeautifulSoup

from rtv.downloader.common import Downloader


class TvpParlamentDL(Downloader):
    _VALID_URL = r'https?://(?:www\.)?tvpparlament\.pl/(?P<show_name>[\w\-.,]+)/'

    @staticmethod
    def get_json_url(*, object_id, sdt_version, **kwargs):
        json_url = f'http://www.tvpparlament.pl/shared/cdn/tokenizer_v2.php' \
                   f'?object_id={object_id}' \
                   f'&std_version={sdt_version}'
        return json_url

    def get_video_data(self):
        self.get_html()
        soup = BeautifulSoup(self.html, 'html.parser')

        pattern = re.compile(r'(?P<video_ids>playVideo\s+=\s+{.*})', re.DOTALL)
        script = soup.find('script', text=pattern)
        match = pattern.search(script.text)

        video_ids_raw = match.group('video_ids')
        video_ids = js2py.eval_js(f'Object({video_ids_raw})').to_dict()

        json_url = self.get_json_url(**video_ids)
        video_data = requests.get(json_url).json()

        return video_data

    def get_podcast_date(self):
        soup = BeautifulSoup(self.html, 'html.parser')

        pattern = re.compile(r'[dD]ata:?\s+(?P<date>\d{2,4}-\d{1,2}-\d{1,2})')
        div = soup.find('div', text=pattern)
        match = pattern.search(div.text)

        date_str = match.group('date')
        podcast_date = datetime.datetime.strptime(date_str, '%Y-%m-%d')

        return podcast_date

    def get_podcast_show_name(self):
        # TODO: scrape show_name from web
        match = re.match(self._VALID_URL, self.url)
        return match.group('show_name').replace('-', ' ').title()

    def get_info(self):
        data = self.get_video_data()

        # choose format providing manifest as it gives much flexibility in terms of quality choice
        entry = next((item for item in data['formats']
                      if item['mimeType'] == 'application/vnd.ms-ss'), None)

        podcast_info = {
            'entries': [{
                'title': data.get('title'),
                'show_name': self.get_podcast_show_name(),
                'date': self.get_podcast_date(),
                'url': entry.get('url'),
                'ext': 'mp4',
            }]
        }

        return podcast_info
