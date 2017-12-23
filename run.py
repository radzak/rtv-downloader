from rtv.RTVdownloader import RTVdownloader
from rtv.options import parse_options
from rtv.onetab import get_urls_from_onetab


def main():
    options, args = parse_options()
    urls = args.urls
    files = args.files
    onetabs = args.onetabs

    rtv_dl = RTVdownloader(options)

    for file in files:
        file_urls = filter(None, (line.strip() for line in file))
        urls.extend(file_urls)

    for onetab in onetabs:
        onetab_urls = get_urls_from_onetab(onetab)
        urls.extend(onetab_urls)

    # TODO: meh :/ solution
    rtv_dl.download(set(urls))
    rtv_dl.run_terminal_ui()


if __name__ == '__main__':
    main()

# TODO: add metadata to file, such as description ect., check if it is already there
# TODO: add max download time and retry?
