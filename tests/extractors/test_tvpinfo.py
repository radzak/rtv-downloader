from rtv.extractors.tvpinfo import TvpInfo

from ..test_extractors import ExtractorTester


class TestVodTVPExtractor(ExtractorTester):
    extractor_class = TvpInfo
    urls = [
        'http://www.tvp.info/35115550/spotkanie-u-prezydenta-zaprosil-premier-i-prezesa-pis'
    ]
