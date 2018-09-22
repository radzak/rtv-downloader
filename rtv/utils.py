import contextlib
import os
import re
import sys
import urllib.parse

import tldextract
import validators

from rtv.exceptions import WrongUrlError


class DevNull:
    """
    DevNull class that has a no-op write and flush method.
    """
    def write(self, *args, **kwargs):
        pass

    def flush(self):
        pass


@contextlib.contextmanager
def suppress_stdout():
    """
    Context manager that suppresses stdout.

    Examples:
        >>> with suppress_stdout():
        ...     print('Test print')

        >>> print('test')
        test

    """
    save_stdout = sys.stdout
    sys.stdout = DevNull()
    yield
    sys.stdout = save_stdout


def validate_url(url):
    """
    Validate url using validators package.

    Args:
        url (str): Url.

    Returns:
        bool: True if valid, False otherwise.

    Examples:
        >>> validate_url('http://google.com')
        True

        >>> validate_url('http://google')  # doctest: +ELLIPSIS
        ValidationFailure(...)

        >>> if not validate_url('http://google'):
        ...     print('not valid')
        not valid

    """
    return validators.url(url)


def get_domain_name(url):
    """
    Extract a domain name from the url (without subdomain).

    Args:
        url (str): Url.

    Returns:
        str: Domain name.

    Raises:
        DomainNotMatchedError: If url is wrong.

    Examples:
        >>> get_domain_name('https://vod.tvp.pl/video/')
        'tvp.pl'

        >>> get_domain_name('https://vod')
        Traceback (most recent call last):
        ...
        rtv.exceptions.WrongUrlError: Couldn't match domain name of this url: https://vod

    """
    if not validate_url(url):
        raise WrongUrlError(f'Couldn\'t match domain name of this url: {url}')

    ext = tldextract.extract(url)
    return f'{ext.domain}.{ext.suffix}'


def clean_video_data(_data):
    """
    Clean video data:
        -> cleans title
        -> ...

    Args:
        _data (dict): Information about the video.

    Returns:
        dict: Refined video data.

    """

    data = _data.copy()

    # TODO: fix this ugliness
    title = data.get('title')
    if title:
        data['title'] = clean_title(title)

    return data


def clean_title(title):
    """
    Clean title -> remove dates, remove duplicated spaces and strip title.

    Args:
        title (str): Title.

    Returns:
        str: Clean title without dates, duplicated, trailing and leading spaces.

    """
    date_pattern = re.compile(r'\W*'
                              r'\d{1,2}'
                              r'[/\-.]'
                              r'\d{1,2}'
                              r'[/\-.]'
                              r'(?=\d*)(?:.{4}|.{2})'
                              r'\W*')
    title = date_pattern.sub(' ', title)
    title = re.sub(r'\s{2,}', ' ', title)
    title = title.strip()
    return title


def clean_filename(filename):
    """
    Remove unsupported filename characters.
    On Windows file names cannot contain any of \/:*?"<>| characters.
    Effectively remove all characters except alphanumeric, -_#.,() and spaces.

    Args:
        filename (str): Name of a file.

    Returns:
        str: Filename without unsupported characters.

    """
    return re.sub('[^\w\-_#.,() ]', '', filename)


def file_exists(path):
    """
    Check whether a file exists.

    Args:
        path (str): Path to a file.

    Returns:
        bool: True if exists, False otherwise.

    """
    return os.path.exists(path)


def get_ext(url):
    """
    Extract an extension from the url.

    Args:
        url (str): String representation of a url.

    Returns:
        str: Filename extension from a url (without a dot), '' if extension is not present.

    """

    parsed = urllib.parse.urlparse(url)
    root, ext = os.path.splitext(parsed.path)
    return ext.lstrip('.')


def delete_duplicates(seq):
    """
    Remove duplicates from an iterable, preserving the order.

    Args:
        seq: Iterable of various type.

    Returns:
        list: List of unique objects.

    """
    seen = set()
    seen_add = seen.add
    return [x for x in seq if not (x in seen or seen_add(x))]
