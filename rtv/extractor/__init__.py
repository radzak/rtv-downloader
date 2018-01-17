from .downloaders import *

_ALL_EXTRACTORS = [
    cls
    for name, cls in globals().items()
    if name.endswith('DL')
    ]


def gen_extractor_classes():
    """
    Return a list of supported extractor classes.
    """
    return _ALL_EXTRACTORS


__all__ = ['gen_extractor_classes']
