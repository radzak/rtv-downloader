import pprint

from rtv.downloaders.youtubedl import YoutubePD
from rtv.utils import clean_video_data


class Field:
    def __init__(self):
        self.name = None

    def __get__(self, instance, owner):
        if instance is None:
            return self
        return instance.data.get(self.name)

    def __set__(self, instance, value):
        raise AttributeError(f"You can't set {self.name} attribute manually.")


class Meta(type):
    def __new__(mcs, name, bases, class_dict):
        for key, value in class_dict.items():
            if isinstance(value, Field):
                value.name = key
        cls = type.__new__(mcs, name, bases, class_dict)
        return cls


class Video(metaclass=Meta):
    title = Field()
    date = Field()
    url = Field()
    ext = Field()

    def __init__(self, data):
        self.data = clean_video_data(data)

    def download(self, **kwargs):
        ypd = YoutubePD(self, **kwargs)
        ypd.download()

    def print_data(self):
        """Pretty print the data of this video."""
        pprint.pprint(self.data)

    def __str__(self):
        return f'Video({self.title})'

    def __repr__(self):
        return f'{self.__class__.__name__}({self.data})'
