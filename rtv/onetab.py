import requests
from bs4 import BeautifulSoup


def get_urls_from_onetab(onetab):
    """
    Get video urls from a link to the onetab shared page.

    Args:
        onetab (str): Link to a onetab shared page.

    Returns:
        list: List of links to the videos.

    """
    html = requests.get(onetab).text
    soup = BeautifulSoup(html, 'lxml')

    divs = soup.findAll('div', {'style': 'padding-left: 24px; '
                                         'padding-top: 8px; '
                                         'position: relative; '
                                         'font-size: 13px;'})

    return [div.find('a').attrs['href'] for div in divs]
