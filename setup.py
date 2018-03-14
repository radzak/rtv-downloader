from pathlib import Path

from setuptools import setup

packages = ['rtv', 'rtv.extractors', 'rtv.downloaders']

requires = [
    'requests',
    'dateparser',
    'Js2Py',
    'youtube_dl',
    'validators',
    'beautifulsoup4',
    'tldextract'
]

about = {}
with Path('rtv', '__version__.py').open('r', encoding='utf-8') as f:
    exec(f.read(), about)

setup(
    name=about['__title__'],
    version=about['__version__'],
    description=about['__description__'],
    url=about['__url__'],
    author=about['__author__'],
    author_email=about['__author_email__'],
    license=about['__license__'],
    packages=packages,
    entry_points={
        'console_scripts': ['rtv=rtv.cli:main'],
    },
    python_requires='>=3.6',
    install_requires=requires,
    setup_requires=['pytest-runner'],
    tests_require=['pytest'],
    zip_safe=False,
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: End Users/Desktop',
        'Topic :: Multimedia :: Video',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.6',
    ]
)
