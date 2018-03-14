from rtv.extractors.tvpparlament import TvpParlament

from ..test_extractors import ExtractorTester


class TestTvpParlamentExtractor(ExtractorTester):
    extractor_class = TvpParlament
    urls = [
        'http://www.tvpparlament.pl/retransmisje-vod/inne/przesluchanie-przez-komisja-ds-amber-gold-b-dyr-biura-kolegium-ds-sluzb-specjalnych-w-kprm-tomasza-borkowskiego/35118797'
    ]
