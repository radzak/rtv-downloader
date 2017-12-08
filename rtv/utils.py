import contextlib
import os
import re
import sys
import urllib.parse


class DevNull:
    def write(self, *args, **kwargs):
        pass

    def flush(self):
        pass


@contextlib.contextmanager
def supress_stdout():
    save_stdout = sys.stdout
    sys.stdout = DevNull()
    yield
    sys.stdout = save_stdout


def get_site_name(url):
    match = re.match(r'^'
                     r'(?:http|https)://'
                     r'(?:www\.)?'
                     r'.*?'
                     r'(?P<site_name>\w+\.\w+)/'
                     r'.*',
                     url)
    if match:
        return match.group('site_name')


def clean_podcast_info(info: dict):
    if 'title' in info:
        info.update(
            title=clean_title(info.pop('title'))
        )


def clean_title(title):
    date_regex = r'\s*' \
                 r'\d{1,2}' \
                 r'[/\-.]' \
                 r'\d{1,2}' \
                 r'[/\-.]' \
                 r'(?=\d*)(?:.{4}|.{2})' \
                 r'\s*'

    title = re.sub(date_regex, ' ', title)
    title = re.sub(r'\s{2,}', ' ', title)
    title = title.strip()
    return title


def clean_filename(filename):
    """
    Remove unsupported filename characters.
    On Windows file names cannot contain any of \/:*?"<>| characters.
    Effectively remove all characters except alphanumeric, -_#.,() and spaces.
    """
    return re.sub('[^\w\-_#.,() ]', '', filename)


def rename_file(path, new_path):
    """
    Rename/move a file and remove unsupported characters from the filename.
    Args:
        path (str): Current path of a file.
        new_path (str): New path to a file.

    Returns:
        None

    """
    location, filename = os.path.split(new_path)
    filename = clean_filename(filename)
    new_path = os.path.join(location, filename)

    os.rename(path, new_path)


def get_ext(url):
    """Return the filename extension from url, or '' if ext. is not present."""
    parsed = urllib.parse.urlparse(url)
    root, ext = os.path.splitext(parsed.path)
    return ext.lstrip('.')
