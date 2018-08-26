from rtv.extractors.wp import Wp

from ..test_extractors import ExtractorTester


class TestWpExtractor(ExtractorTester):
    extractor_class = Wp
    urls = [
        'https://video.wp.pl/i,hofman-do-kempy-nasze-relacje-byly-dosc-chlodne-bo-tupalem-tlustymi-nozkami,mid,2022374,cid,2303876,klip.html'
    ]
