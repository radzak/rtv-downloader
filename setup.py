from setuptools import setup

import rtv

DESCRIPTION = 'RTV podcast downloader'
LONG_DESCRIPTION = 'Command-line program to download podcasts from various sites.'

setup(name='rtv',
      version=rtv.__version__,
      description=DESCRIPTION,
      long_description=LONG_DESCRIPTION,
      url='https://github.com/radzak/RtvDownloader',
      author='Radek Krzak',
      author_email='radek.krzak@gmail.com',
      license='MIT',
      packages=['rtv', 'rtv.downloader', 'rtv.extractor'],
      entry_points={
          'console_scripts': ['rtv=rtv.cli:main'],
      },
      install_requires=[
          'requests',
          'dateparser',
          'Js2Py',
          'youtube_dl',
          'validators',
          'beautifulsoup4'
      ],
      setup_requires=['pytest-runner'],
      tests_require=['pytest'],
      zip_safe=False)
