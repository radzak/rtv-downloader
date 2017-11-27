from rtv.utils import get_site_name
from rtv.downloader import gen_downloader_classes


class RTVdownloader:
    def __init__(self, options=None):
        self.options = options
        self.downloaders = []

        self.add_default_downloaders()

    def download(self, url_list):
        for url in url_list:
            site = get_site_name(url)

            # TODO: fix site matching, fix default template
            name_tmpl = self.options['name_tmpls'].get(site, '{date} abc.mp3')
            dl_path = self.options['dl_path']

            for downloader in self.downloaders:
                if downloader.validate_url(url):
                    downloader.download_podcast(url, dl_path, name_tmpl)
                    break
            else:
                print(f'None of the downloaders can handle this url: {url}')

    def add_default_downloaders(self):
        """
        Add the Downloader classes returned by gen_downloaders to the end of the list.
        """
        for downloader in gen_downloader_classes():
            self.downloaders.append(downloader)
