import os

from rtv.utils import clean_filename, clean_podcast_info, get_domain_name


class PodcastDownloader:
    def __init__(self, podcast, options):
        """ Create a PodcastDownloader object with the given options."""
        self.podcast = podcast
        self.options = options
        self.download_dir = options['dl_path']

    def _real_download(self, path, quality):
        """ Real download process. Redefine in subclasses."""
        raise NotImplementedError('This method must be implemented by subclasses')

    def download(self, quality):
        """
        Download podcast to target location. Choose worst quality by default, to decrease file size.

        Args:
            quality (str): Quality of the video.

        Returns:
            None

        """
        path = self.render_path(quality)
        self._real_download(path, quality)

    def render_path(self, quality):
        """
        Render path by filling the path template with podcast information.

        Args:
            quality (str): String representation of quality ('worst'/'best').

        Returns:
            str: Absolute path with the template values filled in.

        """
        # TODO: Fix defaults (add formatter)
        # https://stackoverflow.com/questions/23407295/default-kwarg-values-for-pythons-str-format-method
        podcast_info = self.podcast.info(quality)
        clean_podcast_info(podcast_info)

        site_name = get_domain_name(self.podcast.url(quality))
        template = self.options['name_tmpls'].get(site_name)

        filename_raw = template.format(**podcast_info)
        filename = clean_filename(filename_raw)
        path = os.path.join(self.download_dir, filename)
        return path
