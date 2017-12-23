import argparse
import os


def parse_options():
    """
    Parse command line arguments, merge them with options and return in a tuple.

    options:
        dl_path (str) - download path for podcasts
        name_tmpls (dict) - name templates:
            key -> site name (domain name)
            value -> name template, you can use:
                {date:format} - date of last modification with a given format, ex. %m %d
                    http://strftime.org/
                {title} - title of podcast (supported only by youtube-dl)

    Returns:
        options, urls

    """
    parser = argparse.ArgumentParser(description='Podcast downloader by radzak.',
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
                            help='text file with urls of sites containing podcasts you '
                                 'wish to download '
                            )

    urls_group.add_argument('-o',
                            type=str,
                            dest='onetabs',
                            metavar='ONETAB',
                            default=[],
                            nargs='*',
                            help='onetab links to sites containing podcasts you wish to download'
                            )

    options = {
        'dl_path': os.path.join(os.path.expanduser('~'), 'Desktop', 'RTV'),
        'name_tmpls': {
            'polskieradio.pl': '{date:%d-%m} {title}.{ext}',
            'tokfm.pl': '{date:%d-%m} {title}.{ext}',
            'radiozet.pl': '{date:%d-%m} {show_name} - {title}.{ext}',
            'tvp.pl': '{date:%d-%m} {title}.{ext}',  # No show name available
            'polsatnews.pl': '{date:%d-%m} {title}.{ext}',
            'vod.pl': '{date:%d-%m} {show_name} {title}.{ext}',
            'ipla.tv': '{date:%d-%m} {title}.{ext}',  # add showname?
            'rmf24.pl': '{date:%d-%m} {title}.{ext}',  # add showname?
            'tvn24.pl': '{date:%d-%m} {title}.{ext}',  # add showname?
            'tvpparlament.pl': '{date:%d-%m} {title}.{ext}',
            'tvp.info': '{date:%d-%m} {title}.{ext}',
        }
    }
    # TODO: Add OneTab links support
    # TODO: Add multithreading
    # TODO: add dir option that defaults to the dl_path

    args = parser.parse_args()
    return options, args
