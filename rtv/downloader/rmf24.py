import datetime
import js2py
import re

from bs4 import BeautifulSoup

from rtv.downloader.common import Downloader
from rtv.utils import get_ext


class Rmf24DL(Downloader):
    _VALID_URL = r'https?://(?:www\.)?rmf24\.pl/'

    def get_podcast_date(self):
        soup = BeautifulSoup(self.html, 'html.parser')
        dates = soup.find('div', class_='article-date')
        date_published_str = dates.find('meta', {'itemprop': 'datePublished'}).attrs['content']

        return datetime.datetime.strptime(date_published_str, '%Y-%m-%dT%H:%M:%S')

    @staticmethod
    def extract_entry(scraped_info):
        """
        Transform scraped_info dictionary into entry, under the assumption that there is only
        one track in 'track' list, since each video/audio is instantiated individually
        on the RMF website and each of them is scraped independently, so there shouldn't be cases
        when there are 2 unrelated tracks in one info_dict.

        Args:
            scraped_info (dict): Podcast info dict, scraped straight from podcast site.

        Returns:
            dict: Entry containing title, formats (url, quality), thumbnail, etc.

        """
        formats = []
        quality_mapping = {  # ascending in terms of quality
            'lo': 0,
            'hi': 1
        }

        entry = scraped_info['tracks'][0]
        '''
        The structure of entry is as follows:

        'src': {
            'hi': [
                {
                'src': 'http://v.iplsc.com/30-11-gosc-marek-jakubiak/0007124B3CGCAE6P-A1.mp4',
                'type': 'video/mp4'
                }
            ],
            'lo': [
                {
                'src': 'http://v.iplsc.com/30-11-gosc-marek-jakubiak/0007124B3CGCAE6P-A1.mp4',
                'type': 'video/mp4'
                }
            ]
        }
        '''
        entry.update(
            **entry['data']
        )
        del entry['data']

        sources = entry['src']
        del entry['src']

        # TODO: #LOW_PRIOR Remove date from title of audio files e.g. '10.06 Gość: Jarosław Gowin'

        for src_name, src in sources.items():
            url = src[0]['src']
            formats.append({
                'url': url,
                'quality': quality_mapping[src_name],
                'ext': get_ext(url),
                'width': int(scraped_info.get('width')),
                'height': int(scraped_info.get('height')),
            })

        entry.update({
            'formats': formats
        })

        return entry

    def scrape_podcast_info(self):
        entries = []

        soup = BeautifulSoup(self.html, 'html.parser')
        pattern = re.compile(r'Video.createInstance\((?P<js_object>{.*?})\);', re.DOTALL)
        scripts = soup.findAll('script', text=pattern)
        for script in scripts or []:
            matches = pattern.findall(script.text)
            for data in matches:  # matches is a list of matched strings, not match objects
                info_dict = js2py.eval_js(f'Object({data})').to_dict()
                entries.append(self.extract_entry(info_dict))

        # temporarily return only audio entries if present, otherwise return all video entries
        audio_entries = [e for e in entries if e.get('type', 'video') == 'audio']
        if audio_entries:
            entries = audio_entries

        return {'entries': entries}

    def get_info(self):
        self.get_html()

        podcast_info = self.scrape_podcast_info()
        self.update_podcast_info_entries(podcast_info, {
            'date': self.get_podcast_date(),
        })
        return podcast_info
