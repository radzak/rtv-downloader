from rtv.RTVdownloader import RTVdownloader
from rtv.options import parse_options


def main():
    options, urls = parse_options()
    rtv_dl = RTVdownloader(options)

    all_urls = [url.strip() for url in set(urls)]
    rtv_dl.download(all_urls)


if __name__ == '__main__':
    main()

# TODO: add metadata to file, such as description ect., check if it is already there
# TODO: add max download time and retry?
