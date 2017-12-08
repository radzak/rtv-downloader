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
