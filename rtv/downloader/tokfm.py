import json
import requests
import urllib.request

from rtv.downloader.common import Downloader


class TokFmDL(Downloader):
    _VALID_URL = r'https?://(?:www\.)?audycje\.tokfm\.pl/.*/(?P<title>[\w-]+)/(?P<podcast_id>[a-z0-9-]*)'

    @classmethod
    def get_real_url(cls, url):
        podcast_id = cls.validate_url(url).group('podcast_id')
        data = {'pid': podcast_id, 'st': 'tokfm'}
        r = requests.post('http://audycje.tokfm.pl/gets', data=json.dumps(data))
        url = json.loads(r.text)['url']
        return url

    @classmethod
    def _real_download(cls, path, url):
        # https://stackoverflow.com/questions/2795331/python-download-without-supplying-a-filename
        urllib.request.urlretrieve(url, f'{path}')

    @classmethod
    def get_info(cls, url):
        return {'title': cls.validate_url(url).group('title'),
                'ext': 'mp3',
                }
