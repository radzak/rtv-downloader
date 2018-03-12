from rtv.extractor.tokfm import TokFm

from ..test_extractors import ExtractorTester


class TestTokFmExtractor(ExtractorTester):
    extractor_class = TokFm
    urls = [
        'http://audycje.tokfm.pl/podcast/Instrukcja-obslugi-nastolatka-Mowi-Olga-Wozniak/56655'
    ]
