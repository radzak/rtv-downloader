import os

from rtv.exceptions import NoTemplateFoundError
from rtv.exceptions import WrongQualityError
from rtv.options import DEFAULT_OPTIONS
from rtv.utils import clean_filename


class PodcastDownloader:
    def __init__(self, podcast, quality=None, download_dir=None, templates=None):
        """
        Create a PodcastDownloader for a given podcast.
        
        Args:
            podcast (Podcast): Podcast object. 
            quality (str): Quality of the video (best/worst). Audio quality defaults to best.
            download_dir (str): Destination directory for the downloaded podcast.
            templates (dict): Dictionary of templates needed to generate a download path.

        """
        self.podcast = podcast
        self.quality = quality or DEFAULT_OPTIONS['quality']
        self.download_dir = download_dir or DEFAULT_OPTIONS['download_dir']
        self.templates = templates or DEFAULT_OPTIONS['templates']
        
        if self.quality not in ('worst', 'best'):
            raise WrongQualityError

    def _real_download(self, path):
        """Real download process. Redefine in subclasses."""
        raise NotImplementedError('This method must be implemented by subclasses')

    def download(self):
        """
        Download podcast to target location. Choose worst quality by default, to decrease file size.

        Returns:
            None

        """
        path = self.render_path()
        self._real_download(path)

    def render_path(self):
        """
        Render path by filling the path template with podcast information.

        Returns:
            str: Absolute path with the template values filled in.

        """
        # TODO: Fix defaults (add formatter)
        # https://stackoverflow.com/questions/23407295/default-kwarg-values-for-pythons-str-format-method

        data = self.podcast.data
        site_name = data['site']

        try:
            template = self.templates[site_name]
        except KeyError:
            raise NoTemplateFoundError

        filename_raw = template.format(**data)
        filename = clean_filename(filename_raw)
        path = os.path.join(self.download_dir, filename)
        return path
