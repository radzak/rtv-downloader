from rtv.RTVdownloader import RTVdownloader
from rtv.options import parse_options


def main():
    options, urls = parse_options()
    rtv_dl = RTVdownloader(options)

    all_urls = [url.strip() for url in urls]
    rtv_dl.download(all_urls)

# Remember to set PYTHONIOENCODING=utf-8
# https://wiki.python.org/moin/PrintFails

# https://superuser.com/questions/312132/command-prompt-hangs-until-keypress
# TURN OFF QUICK EDIT MODE? JESUS CHRIST, WINDOWS SUX ... JUST KILL ME

if __name__ == '__main__':
    main()
    # from youtube_dl import YoutubeDL
    # with YoutubeDL() as ydl:
    #     info_dict = ydl.extract_info('https://vod.tvp.pl/video/warto-rozmawiac,23112017,34669053', download=False)
    #     import pprint
    #     pprint.pprint(info_dict)
    #     pprint.pprint(info_dict['ext'])

# TODO: check if the given URL is an actual URL, validating in downloaders is not enough IMO
# TODO: rethink classmethods vs staticmethods
# TODO: add tests
# TODO: add description to file from get_info (youtube-dl)
# TODO: add max download time and retry?
# TODO: add word boundaries to regexes
# TODO: fix super().get_info(url) multiple times somehow :/
