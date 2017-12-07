import datetime
import re
import sys
import time

import requests

from rtv.downloader.common import Downloader


class VodDL(Downloader):
    _VALID_URL = r'https?://(?:www\.)?vod\.pl/'

    # TODO: Check if youtube-dl works with VOD podcasts
    def _real_download(self, podcast, path, quality):
        with open(path, 'wb') as f:
            start = time.clock()
            r = requests.get(podcast.url(quality), stream=True)
            total_length = int(r.headers.get('content-length'))
            dl = 0
            if total_length is None:  # no content length header
                f.write(r.content)
            else:
                for chunk in r.iter_content(1024):
                    dl += len(chunk)
                    f.write(chunk)
                    done = int(50 * dl / total_length)
                    sys.stdout.write("\r[%s%s] %s Mb/s" % (
                    '=' * done, ' ' * (50 - done), dl // (time.clock() - start) // 1048576))
                    print(end='')

    def get_podcast_date(self):
        match = re.search(r'\'datePublished\'\s+:\s+\'(?P<date>\d{4}-\d{2}-\d{2}).*', self.html)

        if match:
            date_str = match.group('date')
            return datetime.datetime.strptime(date_str, '%Y-%m-%d')

    @staticmethod
    def _extract_podcast_show_name(string):
        """
        Extract podcast show name from a string containing title, show name and sometimes date.
        ex. 'Tomasz Lis.: Joanna Mucha, Michał Kamiński i Cezary Kucharski (9.10)'
        Args:
            string (str): VOD podcast title in raw form.

        Returns:
            re.match object if successful, None otherwise.

        """
        match = re.match(r'^(?P<show_name>[\w#\-.,\s]+):.*$', string)

        if match:
            return match.group('show_name')

    @staticmethod
    def _extract_podcast_title(string):
        """
        Extract podcast title from a string containing title, show name and sometimes date.
        ex. 'Tomasz Lis.: Joanna Mucha, Michał Kamiński i Cezary Kucharski (9.10)'
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

        self.update_podcast_info_entries(podcast_info, {
            'title': self._extract_podcast_title(title_raw),
            'show_name': self._extract_podcast_show_name(show_name_raw),
            'date': self.get_podcast_date(),
            'formats': podcast_info.pop('formats'),  # move
            'url': podcast_info.get('url'),  # copy
            'ext': podcast_info.get('ext'),  # copy
        })
        return podcast_info
