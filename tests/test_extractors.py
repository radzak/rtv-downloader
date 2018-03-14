import pytest


class ExtractorTester:
    extractor_class = None
    urls = []

    # consider it as @pytest.fixture(params=urls) working at collection time
    def pytest_generate_tests(self, metafunc):
        """
        It is basically a parametrized pytest fixture, but due to the fact that
        fixtures still don't work in collection time, this solution is necessary
        to provide a fixture that uses attributes overwritten by subclasses as
        fixture 'params' argument.

        https://docs.pytest.org/en/latest/parametrize.html#pytest-generate-tests

        Args:
            metafunc: pytest fixture-like object.

        """
        if 'url' in metafunc.fixturenames:
            metafunc.parametrize("url",
                                 self.urls,
                                 scope='class')

    @pytest.fixture
    def extractor(self, url):
        ext = self.extractor_class(url)
        ext.run()
        return ext

    def test_url_validation(self, url):
        assert self.extractor_class.validate_url(url)

    def test_videos_loaded(self, extractor):
        assert len(extractor.videos) >= 1

    def test_all_videos_have_neccessary_data(self, extractor):
        videos = extractor.videos

        for video in videos:
            title = video.title
            date = video.date
            url = video.url
            ext = video.ext
            assert title and date and url and ext
