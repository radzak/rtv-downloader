import shlex
import threading

import youtube_dl

from rtv.downloaders.common import VideoDownloader


class YoutubePD(VideoDownloader):
    def _real_download(self, path):
        # TODO: choose the right url and extension if the 'formats' key is present in video data
        quality = self.quality
        url = self.video.url
        ext = self.video.ext

        def run():
            command = (
                f'youtube-dl '
                f'-f {quality}[ext={ext}]/'
                f'{quality}video+bestaudio/bestaudio '
                f'--merge-output-format "{ext}" '
                f'-o "{path}" '
                f'{url}'
            )
            youtube_dl.main(shlex.split(command)[1:])

        t = threading.Thread(target=run)
        t.start()
        t.join()
