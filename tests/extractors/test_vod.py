from rtv.extractors.vod import Vod

from ..test_extractors import ExtractorTester


class TestVodTVPExtractor(ExtractorTester):
    extractor_class = Vod
    urls = [
        'https://vod.pl/programy-onetu/tomasz-lis-joanna-mucha-michal-kaminski-i-cezary-kucharski-910/90hqt84'
    ]
