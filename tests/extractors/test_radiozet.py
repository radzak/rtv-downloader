from rtv.extractor.radiozet import RadioZet

from ..test_extractors import ExtractorTester


class TestRadioZetExtractor(ExtractorTester):
    extractor_class = RadioZet
    urls = [
        'http://www.radiozet.pl/Radio/Programy/Sniadanie-w-Radiu-ZET/Kownacki-Poprzemy-prezydenckie-ustawy-ws.-reformy-sadownictwa-jesli-nie-bedzie-to-tuszowanie-i-pozorowanie-reformy'
    ]
