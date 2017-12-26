from setuptools import setup

DESCRIPTION = 'RTV podcast downloader'
LONG_DESCRIPTION = 'Command-line program to download podcasts from various sites.'

setup(name='rtv',
      version='0.1',
      description=DESCRIPTION,
      long_description=LONG_DESCRIPTION,
      url='https://github.com/radzak/RTVdownloader',
      author='Radek Krzak',
      author_email='radek.krzak@gmail.com',
      license='MIT',
      packages=['rtv', 'rtv.downloader'],
      entry_points={
          'console_scripts': ['rtv=rtv.command_line:main'],
      },
      install_requires=[
          'requests',
          'dateparser',
          'Js2Py',
          'youtube_dl',
          'validators',
          'beautifulsoup4'
      ],
      zip_safe=False)
