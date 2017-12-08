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

    def test_all_podcasts_have_neccessary_info(self, downloader):
        podcasts = downloader.podcasts
        for p in podcasts:
            info = p.info()
            url = info.pop('url')
            title = info.pop('title')
            ext = info.pop('ext')
            date = info.pop('date')
            assert url and title and ext and date

    # def test_path_rendering(self, downloader, rendered_path):
    #     paths = []
    #     for p in downloader.podcasts:
    #         paths.append(downloader.render_path(p))
    #     assert sorted(paths) == sorted(rendered_path)


# TODO: make dl_path as pytest tmpdir, also generate rendered_paths with given filenames and dl_paths

class TestPolskieRadioDownloader(CommonDownloaderTests):
    site_name = 'polskieradio.pl'
    urls = [
        'https://www.polskieradio.pl/9/300/Artykul/1919007,Nowa-konstytucja-Swieto-i-referendum-w-jednym-czasie',
    ]
    rendered_paths = [
        ['/tmp/11-11 Nowa konstytucja. Święto i referendum w jednym czasie (Śniadanie w Trójce).mp3'],
    ]
    options = {
        'dl_path': '/tmp',
        'name_tmpls': {
            'polskieradio.pl': '{date:%d-%m} {title}.{ext}'
        }
    }
    downloader_class = PolskieRadioDL


class TestIplaDownloader(CommonDownloaderTests):
    site_name = 'ipla.tv'
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
            'ipla.tv': '{date:%d-%m} {title}.{ext}'
        }
    }
    downloader_class = IplaDL


class TestPolsatNewsDownloader(CommonDownloaderTests):
    site_name = 'polsatnews.pl'
    urls = [
        'http://www.polsatnews.pl/wideo-program/dorotagawrylukzaprasza-29112017_6496311/',
    ]
    rendered_paths = [
        ['/tmp/30-11 #DorotaGawrylukZaprasza.mp4'],
    ]
    options = {
        'dl_path': '/tmp',
        'name_tmpls': {
            'polsatnews.pl': '{date:%d-%m} {title}.{ext}'
        }
    }
    downloader_class = PolsatNewsDL


class TestRadioZetDownloader(CommonDownloaderTests):
    site_name = 'radiozet.pl'
    urls = [
        'http://www.radiozet.pl/Radio/Programy/Sniadanie-w-Radiu-ZET/Kownacki-Poprzemy-prezydenckie-ustawy-ws.-reformy-sadownictwa-jesli-nie-bedzie-to-tuszowanie-i-pozorowanie-reformy',
    ]
    rendered_paths = [
        ['/tmp/24-09 Sniadanie w Radiu ZET - Kownacki Poprzemy prezydenckie ustawy ws. reformy sadownictwa jesli nie bedzie to tuszowanie i pozorowanie reformy.mp4'],
    ]
    options = {
        'dl_path': '/tmp',
        'name_tmpls': {
            'radiozet.pl': '{date:%d-%m} {title}.{ext}'
        }
    }
    downloader_class = RadioZetDL


class TestTokFmDownloader(CommonDownloaderTests):
    site_name = 'tokfm.pl'
    urls = [
        'http://audycje.tokfm.pl/podcast/Instrukcja-obslugi-nastolatka-Mowi-Olga-Wozniak/56655',
    ]
    rendered_paths = [
        ['/tmp/02-12 Instrukcja obsługi nastolatka. Mówi Olga Woźniak.mp3'],
    ]
    options = {
        'dl_path': '/tmp',
        'name_tmpls': {
            'tokfm.pl': '{date:%d-%m} {title}.{ext}'
        }
    }
    downloader_class = TokFmDL


class TestVodDownloader(CommonDownloaderTests):
    site_name = 'vod.pl'
    urls = [
        'https://vod.pl/programy-onetu/tomasz-lis-joanna-mucha-michal-kaminski-i-cezary-kucharski-910/90hqt84',
    ]
    rendered_paths = [
        ['/tmp/09-10 Tomasz Lis. Joanna Mucha, Michał Kamiński i Cezary Kucharski.mp4'],
    ]
    options = {
        'dl_path': '/tmp',
        'name_tmpls': {
            'vod.pl': '{date:%d-%m} {title}.{ext}'
        }
    }
    downloader_class = VodDL


class TestVodTVPDownloader(CommonDownloaderTests):
    site_name = 'tvp.pl'
    urls = [
        'https://vod.tvp.pl/video/warto-rozmawiac,30112017,34760315',
    ]
    rendered_paths = [
        ['/tmp/'],
    ]
    options = {
        'dl_path': '/tmp',
        'name_tmpls': {
            'tvp.pl': '{date:%d-%m} {title}.{ext}'
        }
    }
    downloader_class = VodTVPDL


class TestRmf24Downloader(CommonDownloaderTests):
    site_name = 'rmf24.pl'
    urls = [
        'http://www.rmf24.pl/tylko-w-rmf24/rozmowa/news-abp-gadecki-o-rozancu-do-granic-przygotowane-nie-przez-ksiez,nId,2449655',
    ]
    rendered_paths = [
        ['/tmp/'],
    ]
    options = {
        'dl_path': '/tmp',
        'name_tmpls': {
            'rmf24.pl': '{date:%d-%m} {title}.{ext}'
        }
    }
    downloader_class = Rmf24DL


class TestTvn24Downloader(CommonDownloaderTests):
    site_name = 'tvn24.pl'
    urls = [
        'https://www.tvn24.pl/politico-ziobro-wsrod-osob-ktore-beda-ksztaltowac-europe-w-2018-roku,796687,s.html',
        'https://www.tvn24.pl/loza-prasowa,25,m/loza-prasowa-26-11-2017,793720.html',
    ]
    rendered_paths = [
        ['/tmp/07-12 Za twarzą cherubinka kryje siępolityczny wojownik. Zbigniew Ziobro w rankingu Politico.mp4'],
        ['/tmp/27-11 Loża prasowa.mp4']
    ]
    options = {
        'dl_path': '/tmp',
        'name_tmpls': {
            'tvn24.pl': '{date:%d-%m} {title}.{ext}'
        }
    }
    downloader_class = Tvn24DL


class TestTvpParlamentDownloader(CommonDownloaderTests):
    site_name = 'tvpparlament.pl'
    urls = [
        'http://www.tvpparlament.pl/retransmisje-vod/inne/przesluchanie-przez-komisja-ds-amber-gold-b-dyr-biura-kolegium-ds-sluzb-specjalnych-w-kprm-tomasza-borkowskiego/35118797',
    ]
    rendered_paths = [
        ['/tmp/06-12 Przesłuchanie przez komisja ds. Amber Gold b. dyr. biura Kolegium ds. służb specjalnych w KPRM Tomasza Borkowskiego.mp4'],
    ]
    options = {
        'dl_path': '/tmp',
        'name_tmpls': {
            'tvpparlament.pl': '{date:%d-%m} {title}.{ext}'
        }
    }
    downloader_class = TvpParlamentDL


class TestTvpInfoDownloader(CommonDownloaderTests):
    site_name = 'tvp.info'
    urls = [
        'http://www.tvp.info/35115550/spotkanie-u-prezydenta-zaprosil-premier-i-prezesa-pis',
    ]
    rendered_paths = [
        ['/tmp/12-07 Spotkanie u prezydenta. Zaprosił premier i prezesa PiS.mp4'],
    ]
    options = {
        'dl_path': '/tmp',
        'name_tmpls': {
            'tvp.info': '{date:%d-%m} {title}.{ext}'
        }
    }
    downloader_class = TvpInfoDL
