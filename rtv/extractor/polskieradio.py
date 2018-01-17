import datetime

from bs4 import BeautifulSoup

from rtv.extractor.common import Extractor


class PolskieRadioDL(Extractor):
    _VALID_URL = r'https?://(?:www\.)?polskieradio\.pl/'

    def get_podcast_date(self):
        self.get_html()
        soup = BeautifulSoup(self.html, 'html.parser')

        # polskieradio puts date into different tags
        date_formats = [
            (('span', ), {'class_': 'time'}, '%d.%m.%Y %H:%M'),
            (('span', ), {'class_': 'date'}, '%d/%m/%Y')
        ]
        for d in date_formats:
            try:
                date_str = soup.find(*d[0], **d[1]).text.strip()
                return datetime.datetime.strptime(date_str, d[2])
            except (ValueError, AttributeError):
                pass

    def get_info(self):
        podcast_info = super().get_info()
        self.update_podcast_info_entries(podcast_info, {
            'date': self.get_podcast_date()
        })
        return podcast_info

# TODO: Add support for all podcasts on this site.
# https://www.polskieradio.pl/10/5370/Artykul/1934652,Bedzie-glosno-24-listopada-godz-1803
