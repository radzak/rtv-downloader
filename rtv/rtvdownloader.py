from rtv.extractor import EXTRACTORS
from rtv.utils import validate_url


class RtvDownloader:
    def __init__(self):
        self.extractors = EXTRACTORS
        self.podcasts = []

    def load_podcasts(self, urls: set):
        for url in urls:
            if not validate_url(url):
                print(f'This is not a valid url: {url}, skipping...')
                continue

            for Extractor in self.extractors:
                if not Extractor.validate_url(url):
                    continue

                extractor = Extractor(url)
                extractor.run()
                self.podcasts.extend(extractor.podcasts)
                break
            else:
                print(f'None of the extractors can handle this url: {url}')

    def download(self, **kwargs):
        """
        Download each of the loaded podcasts.

        Args:
            **kwargs: Optional arguments that PodcastDownloader takes:
                quality (str): Quality of the video ('best'/'worst')
                download_dir (str): Destination directory for the downloaded podcast.
                templates (dict): Dictionary of templates needed to generate a download path.

        Returns:
            None

        """
        for podcast in self.podcasts:
            podcast.download(**kwargs)
