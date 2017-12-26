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

# TODO: add generic downloader?
# TODO: create api to use RTVdownloader without command line
# TODO: add metadata to file, such as description ect., check if it is already there
# TODO: add max download time and retry?
# TODO: https://www.tvn24.pl/loza-prasowa,25,m/loza-prasowa-17-12-2017,799547.html
# TODO: https://www.ipla.tv/Prawy-do-lewego-lewy-do-prawego-do-usuniecia/vod-11450023
# TODO: https://www.ipla.tv/Tak-czy-nie-powod-opuszczenia-szczytu-unijnego-prz/vod-11417723#/r-5 tu sobie poradził chyba
