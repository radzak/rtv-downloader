import os

from rtv.exceptions import NoTemplateFoundError, WrongQualityError
from rtv.options import DEFAULT_OPTIONS
from rtv.utils import clean_filename


class VideoDownloader:
    def __init__(self, video, quality=None, download_dir=None, templates=None) -> None:
        """
        Create a VideoDownloader for a given video.

        Args:
            video (Video): Video object.
            quality (str): Quality of the video (best/worst). Audio quality defaults to best.
            download_dir (str): Destination directory for the downloaded video.
            templates (dict): Dictionary of templates needed to generate a download path.

        """
        self.video = video
        self.quality = quality or DEFAULT_OPTIONS['quality']
        self.download_dir = download_dir or DEFAULT_OPTIONS['download_dir']
        self.templates = templates or DEFAULT_OPTIONS['templates']

        if self.quality not in ('worst', 'best'):
            raise WrongQualityError

    def _real_download(self, path) -> None:
        """Real download process. Redefine in subclasses."""
        raise NotImplementedError('This method must be implemented by subclasses')

    def download(self) -> None:
        """Download video to target location. Choose worst quality by default, to decrease file size."""
        path = self.render_path()
        self._real_download(path)

    def render_path(self) -> str:
        """Render path by filling the path template with video information."""
        # TODO: Fix defaults when date is not found (empty string or None)
        # https://stackoverflow.com/questions/23407295/default-kwarg-values-for-pythons-str-format-method

        from string import Formatter

        class UnseenFormatter(Formatter):
            def get_value(self, key, args, kwds):
                if isinstance(key, str):
                    try:
                        return kwds[key]
                    except KeyError:
                        return key
                else:
                    return super().get_value(key, args, kwds)

        data = self.video.data
        site_name = data['site']

        try:
            template = self.templates[site_name]
        except KeyError:
            raise NoTemplateFoundError

        fmt = UnseenFormatter()
        filename_raw = fmt.format(template, **data)
        filename = clean_filename(filename_raw)
        path = os.path.join(self.download_dir, filename)
        return path
