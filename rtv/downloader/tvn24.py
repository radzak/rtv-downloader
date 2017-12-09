import dateparser
from bs4 import BeautifulSoup

from rtv.downloader.common import Downloader


class Tvn24DL(Downloader):
    _VALID_URL = r'https?://(?:www\..*)?tvn24\.pl/.*'

    def get_podcast_date(self):
        """

        Returns:
            datetime object if successful, None otherwise

        """
        soup = BeautifulSoup(self.html, 'html.parser')

        div = soup.find('div', class_='articleDateContainer')
        time = div.find('time', datetime=True)
        date_str = time['datetime'].strip()

        return dateparser.parse(date_str)

    def get_info(self):
        self.get_html()

        podcast_info = super().get_info()

        title = podcast_info.pop('title')
        formats = podcast_info.pop('formats')
        description = podcast_info.pop('description')
        date = self.get_podcast_date()

        self.update_podcast_info_entries(podcast_info, {
            'title': title,
            'formats': formats,
            'description': description,
            'date': date,
        })
        return podcast_info
