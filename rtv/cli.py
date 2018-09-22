from rtv.onetab import get_urls_from_onetab
from rtv.options import parse_options
from rtv.rtvdownloader import RTVdownloader


def main():
    options, args = parse_options()
    urls = args.urls
    files = args.files
    onetabs = args.onetabs

    rtv = RTVdownloader()

    for file in files:
        file_urls = filter(None, (line.strip() for line in file))
        urls.extend(file_urls)

    for onetab in onetabs:
        onetab_urls = get_urls_from_onetab(onetab)
        urls.extend(onetab_urls)

    rtv.load(set(urls))
    rtv.download(**options)


if __name__ == '__main__':
    main()

# TODO: add generic downloader?
# TODO: add metadata to file, such as description ect., check if it is already there
# TODO: add max download time and retry?
# TODO: https://www.tvn24.pl/loza-prasowa,25,m/loza-prasowa-17-12-2017,799547.html
