from rtv.onetab import get_urls_from_onetab


def test_scraping_urls_from_onetab_link():
    onetab = 'https://www.one-tab.com/page/4PLmXVsmQQym3lk6JPiWLg'
    urls = get_urls_from_onetab(onetab)

    assert len(urls) == 5
