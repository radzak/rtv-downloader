import os
import re
import shlex

import inquirer
import requests
import youtube_dl

from rtv.utils import clean_filename, get_site_name, supress_stdout


class Podcast:
    def __init__(self, initial_data, **kwargs):
        self.url = None
        self.ext = None
        self.title = None

        for key in initial_data:
            setattr(self, key, initial_data[key])
        for key in kwargs:
            setattr(self, key, kwargs[key])

    def print_all_info(self):
        """
        Pretty print all attributes (info) of this podcast instance.
        Returns:
            None

        """
        import pprint
        pprint.pprint(self.__dict__)

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

    def _real_download(self, podcast, path):
        """
        Effective download to current working directory location, using youtube-dl by default.
        Redefine in subclasses.
        Returns:
            None

        """
        command = f'youtube-dl ' \
                  f'-f worst[ext={podcast.ext}]/worstvideo+bestaudio/bestaudio ' \
                  f'--merge-output-format "{podcast.ext}" ' \
                  f'-o "{path}" ' \
                  f'{podcast.url}'
        youtube_dl.main(shlex.split(command)[1:])
        # TODO: add quality/format? option handling

    def download(self):
        """
        Choose podcasts to download and download them to target location.
        Returns:
            None

        """
        download_list = self.choose_podcasts(self.podcasts)  # TODO: one podcast handling
        for podcast in download_list:
            path = self.render_path(podcast)
            self._real_download(podcast, path)

    def render_path(self, podcast):
        """
        Render path by filling the path template with podcast information.
        Args:
            podcast (Podcast): Podcast object.

        Returns:
            str: Absolute path with the template values filled in.

        """

        values = podcast.__dict__  # :/)
        # TODO: Fix defaults (add formatter)
        filename = clean_filename(self.template.format(**values))
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
                #  TODO: add quality choice, add formats field to Podcast,
                # TODO: add support for _real_download(podcast, quality)
                return info_dict

    # TODO: rethink its usage?? is it ever needed to update all entries?
    @staticmethod
    def update_podcast_info_entries(podcast_info: dict, update_dict: dict):
        entries = podcast_info.get('entries', [{}])
        for entry in entries:
            entry.update(update_dict)

        podcast_info['entries'] = entries
