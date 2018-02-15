import datetime
import re

from rtv.extractor.common import Extractor


class VodDL(Extractor):
    _VALID_URL = r'https?://(?:www\.)?vod\.pl/'

    def get_podcast_date(self):
        # TODO: refactor this function, don't implicitly return None
        # TODO: use better date regex?

        # "uploadDate": "2018-02-08 12:14:22+0100"
        match = re.search(
            r'\"uploadDate\"'
            r'\s*:\s*' 
            r'\"(?P<date>\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}\+\d{4})\"'
            r'.*',
            self.html)

        if match:
            date_str = match.group('date')
            return datetime.datetime.strptime(date_str, '%Y-%m-%d %H:%M:%S%z')

    @staticmethod
    def _extract_podcast_show_name(string):
        # TODO: Fix this (and extr. title) shitty docstrings (it doesn't return match object, just string)
        # TODO: dont implicitly return None value when regex not matched
        # TODO: wrap this into separate function which returns match object and connect two regexes
        """
        Extract podcast show name from a string containing title, show name and sometimes date,
        e.g. 'Tomasz Lis.: Joanna Mucha, Michał Kamiński i Cezary Kucharski (9.10)'
        Args:
            string (str): VOD podcast title in raw form.

        Returns:
            re.match object if successful, None otherwise.

        """
        match = re.match(r'^(?P<show_name>[\w#\-.,\s]+):.*$', string)

        if match:
            return match.group('show_name')

    # TODO: check if this shitty solution works for all videos, I doubt it ... rofl, try scraping the website
    @staticmethod
    def _extract_podcast_title(string):
        """
        Extract podcast title from a string containing title, show name and sometimes date,
        e.g. 'Tomasz Lis.: Joanna Mucha, Michał Kamiński i Cezary Kucharski (9.10)'
        Args:
            string (str): VOD podcast title in raw form.

        Returns:
            re.match object if successful, None otherwise.

        """
        match = re.match(
            r'^.*:\s*(?P<title>\b[\w#\-.,\s]+\b)\s*(?:\(\d{1,2}[:.]\d{1,2}\))?$', string)

        if match:
            return match.group('title')

    def get_info(self):
        self.get_html()

        podcast_info = super().get_info()

        # initially title contains both show_name and title
        title_raw = show_name_raw = podcast_info.get('title')
        # TODO: refactor, don't use two variables here

        podcast_info = {
            'entries': [{
                'title': self._extract_podcast_title(title_raw),
                'show_name': self._extract_podcast_show_name(show_name_raw),
                'date': self.get_podcast_date(),
                'url': self.url,
                'ext': 'mp4',
            }]
        }
        return podcast_info
