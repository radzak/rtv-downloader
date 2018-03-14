from rtv.extractors.vodtvp import VodTVP

from ..test_extractors import ExtractorTester


class TestVodTVPExtractor(ExtractorTester):
    extractor_class = VodTVP
    urls = [
        'https://vod.tvp.pl/video/warto-rozmawiac,30112017,34760315'
    ]
