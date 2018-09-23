from rtv.extractors.ipla import Ipla

from ..test_extractors import ExtractorTester


class TestIplaExtractor(ExtractorTester):
    extractor_class = Ipla
    urls = [
        'https://www.ipla.tv/wideo/news/Gosc-Wydarzen/5007380/Gosc-Wydarzen-Pawel-Adamowicz/090c6a4705c443633df966d648040a8a',
        'https://www.ipla.tv/wideo/news/Rozmowa-dnia/5000237/Rozmowa-dnia-prof-Jan-Zielonka/2f90e244a713e9bcce9eabe4bd6105c3'
    ]
