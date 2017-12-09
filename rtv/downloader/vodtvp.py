import datetime
import json
import re

from bs4 import BeautifulSoup

from rtv.downloader.common import Downloader


class VodTVPDL(Downloader):
    _VALID_URL = r'https?://(?:www\.)?vod.tvp\.pl/' \
                 r'.*?' \
                 r'(?:,?(?P<date>[\d\-]+)?)' \
                 r',' \
                 r'(?P<object_id>\d+)'

    def get_podcast_date(self):
        match = re.match(self._VALID_URL, self.url)
        if not match:
            return None

        date_str = match.group('date')
        date_formats = [
            '%d%m%Y',
            '%d%m%Y-%H%M'
        ]
        for d in date_formats:
            try:
                return datetime.datetime.strptime(date_str, d)
            except (ValueError, AttributeError):
                pass

    def get_podcast_show_name(self):
        """
        Get podcast show name from the podcast site. It's located in the div with 'data-hover'
        attribute under the 'title' key.
        Returns:
            str: Podcast show name.

        """
        soup = BeautifulSoup(self.html, 'html.parser')
        div = soup.find('div', attrs={'data-hover': True})
        data = json.loads(div['data-hover'])
        show_name = data.get('title')

        return show_name

    def get_podcast_title(self):
        """
        Get podcast title from the podcast site. It's located in the div with 'data-hover'
        attribute under the 'episodeCount' key.
        Returns:
            str: Podcast title.

        """
        # considered as a worse solution since most of the podcasts have only date in the title
        # soup = BeautifulSoup(self.html, 'html.parser')
        # div = soup.find('div', attrs={'data-hover': True})
        # data = json.loads(div['data-hover'])
        # title = data.get('episodeCount')

        soup = BeautifulSoup(self.html, 'html.parser')
        title = soup.find('meta', {'property': 'og:title'})['content']
        return title

    def get_podcast_description(self):
        """
        Get podcast description from the podcast site. It's located in the meta tag
        with 'og:description' attribute under 'content' attribute.
        Returns:
            str: Podcast description.

        """
        soup = BeautifulSoup(self.html, 'html.parser')
        description = soup.find('meta', {'property': 'og:description'})['content']
        return description

    def get_info(self):
        self.get_html()

        podcast_info = {
            'entries': [{
                'title': self.get_podcast_title(),
                'show_name': self.get_podcast_show_name(),
                'description': self.get_podcast_description(),
                'date': self.get_podcast_date(),
                'url': self.url,
                'ext': 'mp4'
            }]
        }
        return podcast_info
