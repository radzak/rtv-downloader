import re

import requests
import youtube_dl

from rtv.extractor.podcast import Podcast
from rtv.utils import suppress_stdout


class Extractor:
    EXTRACTOR_NAME = None
    _VALID_URL = None

    def __init__(self, url, options):
        self.url = url
        self.options = options

        self.html = None
        self._podcasts = []

        self.load_podcasts()

    @classmethod
    def validate_url(cls, url):
        """
        Check if the Extractor can handle the given url.
        Args:
            url (str): Url of the podcast.

        Returns:
            re.match object or None if the string does not match the pattern.

        """
        match = re.match(cls._VALID_URL, url)
        return match

    @property
    def podcasts(self):
        """
        Returns _podcasts found by subclass of :class:`~rtv.extractor.common.Extractor`

        Returns:
             :py:obj:`list` of :obj:`~rtv.extractor.podcast.Podcast`: List of extracted _podcasts.

        """
        return self._podcasts

    def load_podcasts(self):
        info = self.get_info()
        for entry in info.get('entries'):
            podcast = Podcast(entry)
            self._podcasts.append(podcast)

    # @staticmethod
    # def choose_podcasts(choices):
    #     questions = [
    #         inquirer.Checkbox('_podcasts',
    #                           message="What _podcasts are you interested in?",
    #                           choices=choices,
    #                           ),
    #     ]
    #     answers = inquirer.prompt(questions)
    #     return answers['_podcasts']

    def get_html(self):
        r = requests.get(self.url)
        self.html = r.text

    def get_info(self):
        """
        Get information about _podcasts. Redefine in subclasses.

        Returns:
            dict: Dictionary containing various information such as title, extension, date.

        """
        with suppress_stdout():
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
