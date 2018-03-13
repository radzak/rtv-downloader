import pprint
import sys

from rtv.rtvdownloader import RtvDownloader


def main():
    urls = sys.argv[1:]
    rtv = RtvDownloader()
    rtv.load_podcasts(urls)

    for podcast in rtv.podcasts:
        print(f'[PODCAST DATA]: {podcast}')
        pprint.pprint(podcast.data)
        print()


if __name__ == '__main__':
    main()
