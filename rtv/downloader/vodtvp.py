import datetime
import re

from rtv.downloader.common import Downloader
from rtv.utils import TitleNotMatchedError


class VodTVPDL(Downloader):
    _VALID_URL = r'https?://(?:www\.)?vod.tvp\.pl/.*/(?P<show_name>[\w-]+),(?:[\w-]+-)?(?P<date>\d{8}).*'

    @classmethod
    def get_podcast_date(cls, url):
        date_str = cls.validate_url(url).group('date')
        podcast_date = datetime.datetime.strptime(date_str, '%d%m%Y')
        return podcast_date

    @classmethod
    def get_show_name(cls, url):
        show_name_raw = super().get_info(url).get('title')  # TODO: add error handling if not found
        match = re.match(r'(?P<show_name>.*),(?:.*,)?\s*\d{2}.\d{2}.\d{4}', show_name_raw)

        if match:
            return match.group('show_name')
        else:
            raise TitleNotMatchedError

    @classmethod
    def get_title(cls, url):
        return cls.get_show_name(url)  # These shows have no title, only show_name and description

    # TODO: Scrape title from url and capitalize letters (or from webpage)

    @classmethod
    def get_info(cls, url):
        podcast_info = super().get_info(url)
        podcast_info.update(
            {'title': cls.get_title(url),
             'show_name': cls.get_show_name(url),
             'date': cls.get_podcast_date(url),
             'ext': 'mp4'
             })
        return podcast_info

# TODO: Fix multipliarrrrddrdfrdrd of the get_info method execution
# TODO: Fix youtube_dl.utils.DownloadError: ERROR: tvp:embed said: Materiał niedostępny
