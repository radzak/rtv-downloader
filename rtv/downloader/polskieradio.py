from rtv.downloader.common import Downloader


class PolskieRadioDL(Downloader):
    _VALID_URL = r'https?://(?:www\.)?polskieradio\.pl/'

    @classmethod
    def get_info(cls, url):
        podcast_info = super().get_info(url)
        podcast_info.update({
            'ext': podcast_info['entries'][0].get('ext', 'abc')  # TODO: handle default options in a better way
        })
        return podcast_info
