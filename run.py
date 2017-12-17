from rtv.RTVdownloader import RTVdownloader
from rtv.options import parse_options


def main():
    options, urls, files = parse_options()
    rtv_dl = RTVdownloader(options)

    for file in files:
        file_urls = filter(None, (line.strip() for line in file))
        urls.extend(file_urls)

    # TODO: meh :/ solution
    rtv_dl.download(set(urls))
    rtv_dl.run_terminal_ui()


if __name__ == '__main__':
    main()

# TODO: add metadata to file, such as description ect., check if it is already there
# TODO: add max download time and retry?
