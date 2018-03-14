import pprint
import sys

from rtv.rtvdownloader import RTVdownloader


def main():
    urls = sys.argv[1:]
    rtv = RTVdownloader()
    rtv.load(urls)

    for video in rtv.videos:
        print(f'[VIDEO DATA]: {video}')
        pprint.pprint(video.data)
        print()


if __name__ == '__main__':
    main()
