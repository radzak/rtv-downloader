from rtv.extractor import gen_extractor_classes
from rtv.utils import validate_url


class RtvDownloader:
    def __init__(self, options=None):
        self.options = options
        self.extractors = []

        self.add_default_extractors()

    def download(self, urls: set) -> None:
        for url in urls:
            if not validate_url(url):
                print(f'This is not a valid url: {url}, skipping...')

            for Extractor in self.extractors:
                if Extractor.validate_url(url):
                    extractor = Extractor(url, self.options)
                    extractor.load_podcasts()

                    for podcast in extractor.podcasts:
                        podcast.download(quality='worst')

                    break
            else:
                print(f'None of the extractors can handle this url: {url}')

    def add_default_extractors(self):
        """
        Add Extractor classes returned by :meth:`~rtv.extractor.gen_extractor_classes`
        to the end of the list.
        """
        for extractor in gen_extractor_classes():
            self.extractors.append(extractor)
