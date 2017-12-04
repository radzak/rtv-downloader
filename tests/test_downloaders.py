import pytest

from rtv.downloader.downloaders import *


class CommonDownloaderTests:
    site_name = None
    options = None
    downloader_class = None
    urls = []
    rendered_paths = []

    # consider it as @pytest.fixture(params=urls) working at collection time
    def pytest_generate_tests(self, metafunc):
        """
        It is basically a parametrized pytest fixture, but due to the fact that
        fixtures still don't work in collection time, this solution is necessary
        to provide a fixture that uses attributes overwritten by subclasses as
        fixture 'params' argument.

        https://docs.pytest.org/en/latest/parametrize.html#pytest-generate-tests

        Args:
            metafunc: pytest fixture-like object.

        """
        if 'url' in metafunc.fixturenames:
            metafunc.parametrize("url",
                                 self.urls,
                                 scope='class')
        # idlist = self.urls
        # argnames = ['url', 'rendered_path']
        # argvalues = zip(self.urls, self.rendered_paths)
        # metafunc.parametrize(argnames, argvalues, ids=idlist, scope="class")

    @pytest.fixture
    def downloader(self, url):
        dl = self.downloader_class(url, self.options)
        return dl

    def test_initialization(self, downloader, url):
        dl = downloader
        assert dl.url == url
        assert dl.options == self.options
        assert dl.template == self.options['name_tmpls'][self.site_name]
        assert dl.download_dir == self.options['dl_path']
        assert len(dl.podcasts) > 0

    def test_url_validation(self, url):
        assert self.downloader_class.validate_url(url)

    def test_get_info_contains_nonempty_entries(self, downloader):
        assert downloader.get_info().get('entries')

    def test_get_info_entries_contain_necessary_data(self, downloader):
        entries = downloader.get_info().get('entries')
        for e in entries:
            url = e.pop('url')
            title = e.pop('title')
            ext = e.pop('ext')
            date = e.pop('date')
            assert url and title and ext and date

    # def test_path_rendering(self, downloader, rendered_path):
    #     paths = []
    #     for p in downloader.podcasts:
    #         paths.append(downloader.render_path(p))
    #     assert sorted(paths) == sorted(rendered_path)


# TODO: make dl_path as pytest tmpdir, also generate rendered_paths with given filenames and dl_paths

class TestPolskieRadioDownloader(CommonDownloaderTests):
    site_name = 'polskieradio'
    urls = [
        'https://www.polskieradio.pl/9/300/Artykul/1919007,Nowa-konstytucja-Swieto-i-referendum-w-jednym-czasie',
    ]
    rendered_paths = [
        ['/tmp/11-11 Nowa konstytucja. Święto i referendum w jednym czasie (Śniadanie w Trójce).mp3'],
    ]
    options = {
        'dl_path': '/tmp',
        'name_tmpls': {
            'polskieradio': '{date:%d-%m} {title}.{ext}'
        }
    }
    downloader_class = PolskieRadioDL


class TestIplaDownloader(CommonDownloaderTests):
    site_name = 'ipla'
    urls = [
        'https://www.ipla.tv/Gosc-wydarzen-michal-wojcik/vod-10987691',
        'https://www.ipla.tv/Gosc-wydarzen-mikolaj-wild/vod-10906015',
    ]
    rendered_paths = [
        ['/tmp/17-11 Gość Wydarzeń - Michał Wójcik.mp4'],
        ['/tmp/10-11 Gość Wydarzeń - Mikołaj Wild.mp4'],
    ]
    options = {
        'dl_path': '/tmp',
        'name_tmpls': {
            'ipla': '{date:%d-%m} {title}.{ext}'
        }
    }
    downloader_class = IplaDL


class TestPolsatNewsDownloader(CommonDownloaderTests):
    site_name = 'polsatnews'
    urls = [
        'http://www.polsatnews.pl/wideo-program/dorotagawrylukzaprasza-29112017_6496311/',
    ]
    rendered_paths = [
        ['/tmp/30-11 #DorotaGawrylukZaprasza.mp4'],
    ]
    options = {
        'dl_path': '/tmp',
        'name_tmpls': {
            'polsatnews': '{date:%d-%m} {title}.{ext}'
        }
    }
    downloader_class = PolsatNewsDL


class TestRadioZetDownloader(CommonDownloaderTests):
    site_name = 'radiozet'
    urls = [
        'http://www.radiozet.pl/Radio/Programy/Sniadanie-w-Radiu-ZET/Kownacki-Poprzemy-prezydenckie-ustawy-ws.-reformy-sadownictwa-jesli-nie-bedzie-to-tuszowanie-i-pozorowanie-reformy',
    ]
    rendered_paths = [
        ['/tmp/24-09 Sniadanie w Radiu ZET - Kownacki Poprzemy prezydenckie ustawy ws. reformy sadownictwa jesli nie bedzie to tuszowanie i pozorowanie reformy.mp4'],
    ]
    options = {
        'dl_path': '/tmp',
        'name_tmpls': {
            'radiozet': '{date:%d-%m} {title}.{ext}'
        }
    }
    downloader_class = RadioZetDL


class TestTokFmDownloader(CommonDownloaderTests):
    site_name = 'audycje.tokfm'
    urls = [
        'http://audycje.tokfm.pl/podcast/Instrukcja-obslugi-nastolatka-Mowi-Olga-Wozniak/56655',
    ]
    rendered_paths = [
        ['/tmp/02-12 Instrukcja obsługi nastolatka. Mówi Olga Woźniak.mp3'],
    ]
    options = {
        'dl_path': '/tmp',
        'name_tmpls': {
            'audycje.tokfm': '{date:%d-%m} {title}.{ext}'
        }
    }
    downloader_class = TokFmDL


class TestVodDownloader(CommonDownloaderTests):
    site_name = 'vod'
    urls = [
        'https://vod.pl/programy-onetu/tomasz-lis-joanna-mucha-michal-kaminski-i-cezary-kucharski-910/90hqt84',
    ]
    rendered_paths = [
        ['/tmp/09-10 Tomasz Lis. Joanna Mucha, Michał Kamiński i Cezary Kucharski.mp4'],
    ]
    options = {
        'dl_path': '/tmp',
        'name_tmpls': {
            'vod': '{date:%d-%m} {title}.{ext}'
        }
    }
    downloader_class = VodDL


class TestVodTVPDownloader(CommonDownloaderTests):
    site_name = 'vod.tvp'
    urls = [
        'https://vod.tvp.pl/video/warto-rozmawiac,30112017,34760315',
    ]
    rendered_paths = [
        ['/tmp/'],
    ]
    options = {
        'dl_path': '/tmp',
        'name_tmpls': {
            'vod.tvp': '{date:%d-%m} {title}.{ext}'
        }
    }
    downloader_class = VodTVPDL


class TestRmf24Downloader(CommonDownloaderTests):
    site_name = 'rmf24'
    urls = [
        'http://www.rmf24.pl/tylko-w-rmf24/rozmowa/news-abp-gadecki-o-rozancu-do-granic-przygotowane-nie-przez-ksiez,nId,2449655',
    ]
    rendered_paths = [
        ['/tmp/'],
    ]
    options = {
        'dl_path': '/tmp',
        'name_tmpls': {
            'rmf24': '{date:%d-%m} {title}.{ext}'
        }
    }
    downloader_class = Rmf24DL
