from rtv.extractors.tvn24 import Tvn24

from ..test_extractors import ExtractorTester


class TestTvn24Extractor(ExtractorTester):
    extractor_class = Tvn24
    urls = [
        'https://www.tvn24.pl/politico-ziobro-wsrod-osob-ktore-beda-ksztaltowac-europe-w-2018-roku,796687,s.html',
        'https://www.tvn24.pl/loza-prasowa,25,m/loza-prasowa-26-11-2017,793720.html',
        'https://faktypofaktach.tvn24.pl/aleksander-hall-monika-platek-i-ryszard-bugaj-w-faktach-po-faktach,802854.html'
    ]
