import os
import re
import subprocess
import sys
import urllib.parse

from rtv.nbstreamreader import NonBlockingStreamReader as NBSR


# TODO: Find a good place for Exceptions
# TODO: Check if you can pass info to exception so it gets printed when occurs
class UrlNotMatchedError(Exception):
    pass


class DateNotMatchedError(Exception):
    pass


class TitleNotMatchedError(Exception):
    pass


def run_command(command, file=sys.stdout):
    p = subprocess.Popen(command, stdout=subprocess.PIPE)
    # while True:
    #     out = p.stdout.read(1)
    #     if out == '' and not p.poll():
    #         break
    #     if out != '':
    #         file.write(out.decode())
    #         file.flush()

    while True:
        out = p.stdout.read(1)
        if not out:  # TODO: try if out print out, additionaly if not p.poll(): break
            break
        file.write(out.decode())
        file.flush()
    p.wait()


def get_site_name(url):
    match = re.search(r'(?:http|https)://(?:www\.)?(?P<site_name>[\w.]+)\..*', url)
    if match:
        return match.group('site_name')
    else:
        raise UrlNotMatchedError


def clean_filename(filename):
    """
    Remove unsupported filename characters.
    On Windows filenames cannot contain any of \/:*?"<>| characters.
    Effectively remove all characters except alphanumeric, -_#., and spaces.
    """
    return re.sub('[^\w\-_#., ]', '', filename)


def get_ext(url):
    """Return the filename extension from url, or ''."""
    parsed = urllib.parse.urlparse(url)
    root, ext = os.path.splitext(parsed.path)
    return ext.lstrip('.')
