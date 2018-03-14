import dateparser
import datetime
from bs4 import BeautifulSoup

from rtv.extractors.common import Extractor


class Tvn24(Extractor):
    SITE_NAME = 'tvn24.pl'
    _VALID_URL = r'https?://(?:www\.)?(?:.*\.)?tvn24\.pl/.*'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.get_html()
        self.soup = BeautifulSoup(self.html, 'html.parser')

    def get_date(self):
        div = self.soup.find('div', class_='articleDateContainer')
        time_tag = div.find('time', datetime=True)
        date_str = time_tag['datetime'].strip()
        time_str = div.find('span').text

        date = dateparser.parse(date_str)
        time = dateparser.parse(time_str).time()

        full_date = datetime.datetime.combine(date, time)
        return full_date

    def extract(self):
        entry = self.get_info()
        entry['date'] = self.get_date()

        return [entry]
