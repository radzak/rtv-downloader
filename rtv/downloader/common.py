import os
import re
import shlex

import inquirer
import requests
import youtube_dl

from rtv.utils import clean_filename, get_site_name, supress_stdout
from rtv.exceptions import WrongQualityError


class Podcast:
    def __init__(self, podcast_data):
        self.data = podcast_data

    def choose_format(self, quality):
        quality_func = {
            'worst': min,
            'best': max
        }
        formats = self.data.get('formats')
        if formats:
            func = quality_func[quality]
            choice = func(formats, key=lambda f: f.get('quality') or f.get('height'))

            # TODO: Fix IT!!!! it might mix quality with height
            # In[5]: min([{'height': 24}, {'quality': 23, 'height': 0}], key=lambda f: f.get(
            #     ...: 'quality') or f.get('height'))
            # Out[5]: {'height': 0, 'quality': 23}
        else:
            choice = self.data
            # not sure about clarity, but self.data contains all format information
            # if there is not 'formats' key in the dictionary
        return choice

    def info(self, quality='worst'):
        """
        Get podcast info, depending on the given quality. If there are no formats in podcast data,
        return the values associated with the entire podcast, not with any specific quality.
        Args:
            quality (str): String representation of quality ('worst'/'best'), worst by default.

        Returns:
            dict: Dictionary containing most important information about the podcast of given
            quality, i.e. url, ext, but also more general information such as title, show name,
            date.

        """

        f = self.choose_format(quality)
        return {
            'title': self.data.get('title'),
            'show_name': self.data.get('show_name'),
            'date': self.data.get('date'),

            # format specific data
            'url': f.get('url'),
            'ext': f.get('ext'),
        }

    def ext(self, quality: str) -> str:
        data = self.info(quality)
        return data['ext']

    def url(self, quality: str) -> str:
        data = self.info(quality)
        return data['url']

    @property
    def title(self):
        return self.data.get('title')

    def print_data(self):
        """
        Pretty print all attributes (info) of this podcast instance.
        Returns:
            None

        """
        import pprint
        pprint.pprint(self.data)

    def __repr__(self):
        return f"<Podcast {{'url': '{self.url}', 'title': '{self.title}'}}>"

    def __str__(self):
        return self.title


class Downloader:
    _VALID_URL = None  # Redefine in subclasses.

    def __init__(self, url, options):
        self.url = url
        self.options = options

        self.html = None
        self.template = None
        self.download_dir = None
        self.podcasts = []

        self.load_options()
        self.get_podcast_entries()

    @classmethod
    def validate_url(cls, url):
        """
        Check if the Downloader can handle the given url.
        Args:
            url (str): Url of the podcast.

        Returns:
            re.match object or None if the string does not match the pattern.

        """
        match = re.match(cls._VALID_URL, url)
        return match

    def load_options(self):
        site_name = get_site_name(self.url)
        self.template = self.options['name_tmpls'].get(site_name)
        self.download_dir = self.options['dl_path']

    def get_podcast_entries(self):
        info = self.get_info()
        for entry in info.get('entries'):
            podcast = Podcast(entry)
            self.podcasts.append(podcast)

    @staticmethod
    def choose_podcasts(choices):
        questions = [
            inquirer.Checkbox('podcasts',
                              message="What podcasts are you interested in?",
                              choices=choices,
                              ),
        ]
        answers = inquirer.prompt(questions)
        return answers['podcasts']

    def get_html(self):
        r = requests.get(self.url)
        self.html = r.text

    def _real_download(self, podcast, path, quality):
        """
        Effective download to current working directory location, using youtube-dl by default.
        Redefine in subclasses.
        Args:
            podcast (Podcast):
            path (str):
            quality (str): Quality of the video (best/worst). Audio quality defaults to best.

        Returns:
            None

        """
        if quality not in ('worst', 'best'):
            raise WrongQualityError

        command = f'youtube-dl ' \
                  f'-f {quality}[ext={podcast.ext(quality)}]/{quality}video+bestaudio/bestaudio ' \
                  f'--merge-output-format "{podcast.ext(quality)}" ' \
                  f'-o "{path}" ' \
                  f'{podcast.url(quality)}'
        youtube_dl.main(shlex.split(command)[1:])

    def download(self, quality=None):
        """
        Choose podcasts to download and download them to target location. Choose worst quality
        by default, to decrease file size.
        Returns:
            None

        """
        if not quality:
            quality = self.options.get('quality', 'worst')

        download_list = self.choose_podcasts(self.podcasts)  # TODO: one podcast handling
        for podcast in download_list:
            path = self.render_path(podcast, quality)
            self._real_download(podcast, path, quality)

    def render_path(self, podcast, quality):
        """
        Render path by filling the path template with podcast information.
        Args:
            podcast (Podcast): Podcast object.
            quality (str): String representation of quality ('worst'/'best').

        Returns:
            str: Absolute path with the template values filled in.

        """
        # TODO: Fix defaults (add formatter)

        filename_raw = self.template.format(**podcast.info(quality))
        filename = clean_filename(filename_raw)
        path = os.path.join(self.download_dir, filename)

        return path

    def get_info(self):
        """
        Get information about podcasts. Redefine in subclasses.
        Returns:
            dict: Dictionary containing various information such as title, extension, date.

        """
        with supress_stdout():
            with youtube_dl.YoutubeDL() as ydl:
                info_dict = ydl.extract_info(self.url, download=False)
                return info_dict

    # TODO: rethink its usage?? is it ever needed to update all entries?
    @staticmethod
    def update_podcast_info_entries(podcast_info: dict, update_dict: dict):
        entries = podcast_info.get('entries', [{}])
        for entry in entries:
            entry.update(update_dict)

        podcast_info['entries'] = entries
