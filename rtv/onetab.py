import requests
from bs4 import BeautifulSoup


def get_urls_from_onetab(onetab):
    """
    Get urls... from onetab hyperlink.
    """
    html = requests.get(onetab).text
    soup = BeautifulSoup(html, 'html.parser')

    divs = soup.findAll('div', {'style': 'padding-left: 24px; padding-top: 8px; position: relative; font-size: 13px;'})

    return [div.find('a').attrs['href'] for div in divs]
