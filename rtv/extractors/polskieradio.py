import datetime

from bs4 import BeautifulSoup

from rtv.extractors.common import Extractor


class PolskieRadio(Extractor):
    SITE_NAME = 'polskieradio.pl'
    _VALID_URL = r'https?://(?:www\.)?polskieradio\.pl/'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.load_html()
        self.soup = BeautifulSoup(self.html, 'lxml')

    def get_date(self):
        # polskieradio puts date into different tags
        date_formats = [
            (('span', ), {'class_': 'time'}, '%d.%m.%Y %H:%M'),
            (('span', ), {'class_': 'date'}, '%d/%m/%Y')
        ]
        for d in date_formats:
            try:
                date_str = self.soup.find(*d[0], **d[1]).text.strip()
                return datetime.datetime.strptime(date_str, d[2])
            except (ValueError, AttributeError):
                pass

    def extract(self):
        video_info = self.get_info()
        entries = video_info['entries']

        for entry in entries:
            entry.update({
                'date': self.get_date()
            })

        return entries

# TODO: Add support for all videos on this site.
# https://www.polskieradio.pl/10/5370/Artykul/1934652,Bedzie-glosno-24-listopada-godz-1803
# TODO: Scrape show name
