from rtv.extractors.polskieradio import PolskieRadio

from ..test_extractors import ExtractorTester


class TestPolskieRadioExtractor(ExtractorTester):
    extractor_class = PolskieRadio
    urls = [
        'https://www.polskieradio.pl/9/300/Artykul/1919007,Nowa-konstytucja-Swieto-i-referendum-w-jednym-czasie'
    ]
