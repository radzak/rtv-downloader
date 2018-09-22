import argparse
from pathlib import Path

DEFAULT_OPTIONS = {
    'download_dir': Path.home() / 'Desktop' / 'RTV',
    'templates': {
        'ipla.tv': '{date:%d} {title}.{ext}',
        'polsatnews.pl': '{date:%d} {title}.{ext}',
        'polskieradio.pl': '{date:%d} {title}.{ext}',
        'radiozet.pl': '{date:%d} {show_name} - {title}.{ext}',
        'rmf24.pl': '{date:%d} {title}.{ext}',
        'tokfm.pl': '{date:%d} {title}.{ext}',
        'tvn24.pl': '{date:%d} {title}.{ext}',
        'tvp.info': '{date:%d} {title}.{ext}',
        'tvp.pl': '{date:%d} {title}.{ext}',
        'tvpparlament.pl': '{date:%d} {title}.{ext}',
        'vod.pl': '{date:%d} {show_name} - {title}.{ext}',
        'wp.pl': '{date:%d} {show_name} - {title}.{ext}'
    },
    'quality': 'worst'
}


def parse_options():
    """
    Parse command line arguments.

    Returns:
        options, args

    """
    parser = argparse.ArgumentParser(description='Video downloader by radzak.',
                                     prog='RTVdownloader')
    urls_group = parser.add_mutually_exclusive_group(required=True)
    urls_group.add_argument('urls',
                            type=str,
                            metavar='URL',
                            default=[],
                            nargs='*',
                            help='urls of sites containing videos you wish to download'
                            )

    urls_group.add_argument('-f',
                            type=argparse.FileType('r'),
                            dest='files',
                            metavar='FILE',
                            default=[],
                            nargs='*',
                            help='text file with urls of sites containing videos you '
                                 'wish to download '
                            )

    urls_group.add_argument('-o',
                            type=str,
                            dest='onetabs',
                            metavar='ONETAB',
                            default=[],
                            nargs='*',
                            help='onetab links containing urls of the videos you wish to download'
                            )

    options = DEFAULT_OPTIONS

    # TODO: add dir option that defaults to the DEFAULT_OPTIONS['dl_path']

    args = parser.parse_args()
    return options, args
