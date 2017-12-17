import threading
from multiprocessing import Queue

import validators

from rtv.downloader import gen_downloader_classes
from rtv.terminal_ui import TerminalUI


class RTVdownloader:
    def __init__(self, options=None):
        self.options = options
        self.downloaders = []
        self.queue = Queue()
        self.ui = TerminalUI('RTV podcast downloader by radzak', self.queue)

        self.add_default_downloaders()  # ???

    def download(self, url_list):
        def run():
            for url in url_list:
                if not validators.url(url):
                    print(f'This is not a valid url: {url}, skipping...')
                    continue

                for DL in self.downloaders:
                    if DL.validate_url(url):
                        downloader = DL(url, self.options, self.queue)
                        downloader.download(quality='worst')

                        # import pprint
                        # pprint.pprint(downloader.get_info())
                        break
                else:
                    print(f'None of the downloaders can handle this url: {url}')

        threading.Thread(target=run).start()

    def run_terminal_ui(self):
        self.ui.loop()

    def add_default_downloaders(self):
        """
        Add the Downloader classes returned by gen_downloaders to the end of the list.
        """
        for downloader in gen_downloader_classes():
            self.downloaders.append(downloader)
