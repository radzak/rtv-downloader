import validators

from rtv.downloader import gen_downloader_classes


class RTVdownloader:
    def __init__(self, options=None):
        self.options = options
        self.downloaders = []

        self.add_default_downloaders()  # ???

    def download(self, url_list):
        for url in url_list:
            if not validators.url(url):
                print(f'This is not a valid url: {url}, skipping...')
                continue

            for DL in self.downloaders:
                if DL.validate_url(url):
                    downloader = DL(url, self.options)
                    downloader.download(quality='worst')

                    # print(downloader.podcasts)
                    # import pprint
                    # pprint.pprint(downloader.get_info())
                    # downloader.podcasts[1].print_data()
                    break
            else:
                print(f'None of the downloaders can handle this url: {url}')

    def add_default_downloaders(self):
        """
        Add the Downloader classes returned by gen_downloaders to the end of the list.
        """
        for downloader in gen_downloader_classes():
            self.downloaders.append(downloader)
