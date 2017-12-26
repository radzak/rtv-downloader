import pprint
import sys

import youtube_dl


def main():
    for url in sys.argv[1:]:
        with youtube_dl.YoutubeDL() as ydl:
            info_dict = ydl.extract_info(url, download=False)
            pprint.pprint(info_dict)


if __name__ == '__main__':
    main()
