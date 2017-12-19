import youtube_dl
import pprint

url = input("Podaj url: ")

with youtube_dl.YoutubeDL() as ydl:
    info_dict = ydl.extract_info(url, download=False)
    pprint.pprint(info_dict)
