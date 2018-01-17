import shlex
import threading

import youtube_dl

from rtv.downloader.common import PodcastDownloader
from rtv.exceptions import WrongQualityError


class YoutubePD(PodcastDownloader):
    def _real_download(self, path, quality):
        """
        Effective download, using youtube-dl by default.
        Redefine in subclasses.
        Args:
            path (str):
            quality (str): Quality of the video (best/worst). Audio quality defaults to best.

        Returns:
            None

        """
        if quality not in ('worst', 'best'):
            raise WrongQualityError

        url = self.podcast.url(quality)
        ext = self.podcast.ext(quality)

        def run():
            command = f'youtube-dl ' \
                      f'-f {quality}[ext={ext}]/' \
                      f'{quality}video+bestaudio/bestaudio ' \
                      f'--merge-output-format "{ext}" ' \
                      f'-o "{path}" ' \
                      f'{url}'
            youtube_dl.main(shlex.split(command)[1:])

        # TODO: add information to docstring about this
        t = threading.Thread(target=run)
        t.start()
        t.join()
