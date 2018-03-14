import pprint

from rtv.downloaders.youtubedl import YoutubePD
from rtv.utils import clean_video_data


class Video:
    def __init__(self, data):
        self.data = clean_video_data(data)

    def download(self, **kwargs):
        ypd = YoutubePD(self, **kwargs)
        ypd.download()

    @property
    def title(self):
        return self.data.get('title')

    @property
    def date(self):
        return self.data.get('date')

    @property
    def url(self):
        return self.data.get('url')

    @property
    def ext(self):
        return self.data.get('ext')

    def print_data(self):
        """Pretty print the data of this video."""
        pprint.pprint(self.data)

    def __str__(self):
        return f'Video - {self.title}'
