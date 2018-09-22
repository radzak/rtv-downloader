from datetime import datetime

import dateparser
from bs4 import BeautifulSoup

from rtv.extractors.common import Entries, Extractor


class Tvn24(Extractor):
    SITE_NAME = 'tvn24.pl'
    _VALID_URL = r'https?://(?:www\.)?(?:.*\.)?tvn24\.pl/.*'

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.load_html()
        self.soup = BeautifulSoup(self.html, 'lxml')

    def get_date(self) -> datetime:
        div = self.soup.select_one('div.articleDateContainer')
        time_tag = div.find('time', datetime=True)
        date_str = time_tag['datetime'].strip()
        time_str = div.find('span').text

        date = dateparser.parse(date_str)
        time = dateparser.parse(time_str).time()

        full_date = datetime.combine(date, time)
        return full_date

    def extract(self) -> Entries:
        entry = self.get_info()
        entry['date'] = self.get_date()
        return [entry]
