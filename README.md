# RTVdownloader

Download videos from Ipla.tv, Vod and other Polish video platforms.

### Supported video platforms 

* [Ipla.tv](https://www.ipla.tv/)
* [Vod](https://vod.pl/)
* [Vod.tvp.pl](https://vod.tvp.pl/)
* [Polsat News](www.polsatnews.pl/)
* [TVN24](https://www.tvn24.pl/)
* [PolskieRadio.pl](https://www.polskieradio.pl/)
* [Radio ZET](www.radiozet.pl/)
* [RMF 24](www.rmf24.pl/)
* [Tokfm.pl](http://www.tokfm.pl/)
* [TVP INFO](https://www.tvp.info/)
* [TVP Parlament](www.tvpparlament.pl/)

## Getting Started

### Prerequisites

Make sure you have [ffmpeg](https://www.ffmpeg.org/download.html) installed, since sometimes it's necessary to convert the downloaded video to `mp4` format.

You also need [Python 3.6](https://www.python.org/downloads/) or higher installed on your device.

### Installation

To install RTVdownloader, simply use [pipenv](https://github.com/pypa/pipenv) (or pip, of course):

```bash
pipenv install git+https://github.com/radzak/RTVdownloader.git#egg=rtv
```

## Usage example

### in command-line

```bash
rtv https://vod.tvp.pl/video/warto-rozmawiac,30112017,34760315
```

You can also read links from text files

```bash
rtv -f urls.txt urls2.txt
```

#### [Onetab](https://www.one-tab.com/) support

![demo](https://media.giphy.com/media/65GAmVtwFM9Ba554ci/giphy.gif)

```bash
rtv -o https://www.one-tab.com/page/IgcP09iKQ6GjwDpS-qxKbQ
```

### as a Python package

```python
from rtv import RTVdownloader

urls = ['https://www.ipla.tv/wideo/news/Gosc-Wydarzen/5007380/Gosc-Wydarzen-Pawel-Adamowicz/090c6a4705c443633df966d648040a8a']

rtv = RTVdownloader()
rtv.load(urls)
rtv.download()
```

You can easily inspect the data of the video 

```python
video = rtv.videos[0]

>>> video.data
{
  'date': datetime.datetime(2018, 2, 21, 0, 0),
  'ext': 'mp4',
  'showname': 'Gość Wydarzeń',
  'site': 'ipla.tv',
  'title': 'Gość Wydarzeń - Paweł Adamowicz',
  'url': 'http://redirector.redefine.pl/vm2movies/4homg3f3s1x3t5az2pgsijatktx5c9hn.mp4'
}
```
 
## Development setup

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

```bash
git clone https://github.com/radzak/RTVdownloader.git
cd RTVdownloader
pipenv install
pipenv install --dev
pipenv shell
```

## Running the tests

You can run tests with setup.py

```bash
python setup.py test
```

or with pytest directly

```bash
pytest
``` 

## Contributing

Please read [CONTRIBUTING.md](https://gist.github.com/PurpleBooth/b24679402957c63ec426) for details on our code of conduct, and the process for submitting pull requests to us.

## Authors

* **Radosław Krzak** - [radzak](https://github.com/radzak)

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details
