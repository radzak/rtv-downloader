import dateparser
import datetime
from bs4 import BeautifulSoup

from rtv.extractor.common import Extractor


class Tvn24DL(Extractor):
    _VALID_URL = r'https?://(?:www\.)?(?:.*\.)?tvn24\.pl/.*'

    def get_podcast_date(self):
        """

        Returns:
            datetime object if successful, None otherwise

        """
        soup = BeautifulSoup(self.html, 'html.parser')

        div = soup.find('div', class_='articleDateContainer')
        time_tag = div.find('time', datetime=True)
        date_str = time_tag['datetime'].strip()
        time_str = div.find('span').text

        date = dateparser.parse(date_str)
        time = dateparser.parse(time_str).time()

        full_date = datetime.datetime.combine(date, time)

        return full_date

    def get_title(self):
        soup = BeautifulSoup(self.html, 'html.parser')

        title = soup.find('title').text
        return title

    def get_info(self):
        self.get_html()

        podcast_info = super().get_info()

        title = self.get_title()
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
