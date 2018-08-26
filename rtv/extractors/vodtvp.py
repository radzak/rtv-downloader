import datetime
import json
import re

from bs4 import BeautifulSoup

from rtv.extractors.common import Extractor


class VodTVP(Extractor):
    SITE_NAME = 'vod.tvp.pl'
    _VALID_URL = (
        r'https?://(?:www\.)?vod.tvp\.pl/'
        r'.*?'
        r'(?:,(?P<date>[\d\-]+))?'
        r','
        r'(?P<object_id>\d+)'
    )
    # TODO: change _VALID_URLs to just plain domain name and move date, showname, etc. regexes
    # to functions, so the downloader matches the url despite of absence of additional
    # parameters in the url then the get_x functions will just return None and the Formatter
    # will take care of default values

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.load_html()
        self.soup = BeautifulSoup(self.html, 'lxml')

    def get_date(self):
        match = re.match(self._VALID_URL, self.url)

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

    def get_show_name(self):
        """
        Get video show name from the website. It's located in the div with 'data-hover'
        attribute under the 'title' key.

        Returns:
            str: Video show name.

        """
        div = self.soup.find('div', attrs={'data-hover': True})
        data = json.loads(div['data-hover'])
        show_name = data.get('title')

        return show_name

    def get_title(self):
        """
        Get Video title from the website. It's located in the div with 'data-hover'
        attribute under the 'episodeCount' key.

        Returns:
            str: Video title.

        """
        # considered as a worse solution since most of the videos have only date in the title
        # soup = BeautifulSoup(self.html, 'lxml')
        # div = soup.find('div', attrs={'data-hover': True})
        # data = json.loads(div['data-hover'])
        # title = data.get('episodeCount')

        # TODO: _og_search_title/_og_search_description common method
        title = self.soup.find('meta', {'property': 'og:title'})['content']
        return title

    def get_description(self):
        """
        Get video description from the website. It's located in the meta tag
        with 'og:description' attribute under 'content' attribute.

        Returns:
            str: Video description.

        """
        description = self.soup.find('meta', {'property': 'og:description'})['content']
        return description

    def extract(self):
        entries = [{
            'title': self.get_title(),
            'show_name': self.get_show_name(),
            'description': self.get_description(),
            'date': self.get_date(),
            'url': self.url,
            'ext': 'mp4'
        }]

        return entries
