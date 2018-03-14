from typing import Iterable

from rtv.extractors import EXTRACTORS
from rtv.utils import validate_url


class RTVdownloader:
    def __init__(self):
        self.extractors = EXTRACTORS
        self.videos = []

    def load(self, urls: Iterable):
        for url in urls:
            if not validate_url(url):
                print(f'This is not a valid url: {url}, skipping...')
                continue

            for Extractor in self.extractors:
                if not Extractor.validate_url(url):
                    continue

                extractor = Extractor(url)
                extractor.run()
                self.videos.extend(extractor.videos)
                break
            else:
                print(f'None of the extractors can handle this url: {url}')

    def download(self, **kwargs):
        """
        Download each of the loaded videos.

        Args:
            **kwargs: Optional arguments that VideoDownloader takes:
                quality (str): Quality of the video ('best'/'worst')
                download_dir (str): Destination directory for the downloaded video.
                templates (dict): Dictionary of templates needed to generate a download path.

        Returns:
            None

        """
        for video in self.videos:
            video.download(**kwargs)
