from rtv.RTVdownloader import RTVdownloader
from rtv.options import parse_options


def main():
    options, urls = parse_options()
    rtv_dl = RTVdownloader(options)

    all_urls = [url.strip() for url in set(urls)]
    rtv_dl.download(all_urls)


if __name__ == '__main__':
    main()

# TODO: add description to file from get_info (youtube-dl)
# TODO: add max download time and retry?

# TODO: add support for tvp.info http://www.tvp.info/437819/minela-dwudziesta
# TODO: add support for https://www.tvn24.pl/loza-prasowa,25,m
# TODO: add support for https://faktypofaktach.tvn24.pl/
