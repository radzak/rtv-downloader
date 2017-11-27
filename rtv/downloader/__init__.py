from .downloaders import *

_ALL_CLASSES = [
    cls
    for name, cls in globals().items()
    if name.endswith('DL')
    ]


def gen_downloader_classes():
    """
    Return a list of supported downloader classes.
    """
    return _ALL_CLASSES


def gen_downloaders():
    """ Return a list of an instance of every supported downloader."""
    return [cls() for cls in gen_downloader_classes()]
