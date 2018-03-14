import pytest
import os
import sys
from io import StringIO

from rtv.utils import (delete_duplicates,
                       get_ext,
                       file_exists,
                       clean_filename,
                       clean_title,
                       clean_video_data,
                       get_domain_name,
                       suppress_stdout
                       )

from rtv.exceptions import WrongUrlError


@pytest.mark.parametrize('sequence_type', [
    list,
    tuple
])
def test_deleting_duplicates(sequence_type):
    duplicates = sequence_type([1, 2, 3, 1, 2, 5, 1, 10])
    assert delete_duplicates(duplicates) == [1, 2, 3, 5, 10]


@pytest.mark.parametrize('url, ext', [
    ('http://www.diveintopython3.net/unit-testing.html', 'html'),
    ('media.onet.pl/_ms/88bf013a-3630-4776-8f03-79a400fef5c2.1507555320.064971.mp4', 'mp4'),
    ('https://github.com/requests/requests', ''),
    ('http://google.com', '')
])
def test_extracting_extension_from_url(url, ext):
    assert get_ext(url) == ext


@pytest.mark.parametrize('filename, exists', [
    ('test.txt', True),
    ('idontexist.txt', False),
])
def test_checking_if_file_exists(tmpdir, filename, exists):
    # create test.txt file in temporary directory
    tmpdir.join('test.txt').write('Test content')

    # create a path to the file whose existence we want to check
    path = os.path.join(tmpdir, filename)

    assert file_exists(path) == exists


@pytest.mark.parametrize('dirty_name, name', [
    (r'dirty:file?1\abc<>test|name*yes/no.txt', r'dirtyfile1abctestnameyesno.txt'),
    (r'#test-file_name, (123).txt', r'#test-file_name, (123).txt'),

])
def test_cleaning_filename(dirty_name, name):
    assert clean_filename(dirty_name) == name


@pytest.mark.parametrize('dirty_title, title', [
    ('12/03/2016 video', 'video'),
    ('     video 12-03-2016   ', 'video'),
    ('12.03.16      video 12-03-16  ', 'video'),
])
def test_cleaning_title(dirty_title, title):
    assert clean_title(dirty_title) == title


def test_cleaning_video_data():
    data = {
        'title': '  video 12-03-16  ',
        'url': 'http://test.it/video.mp4',
        'ext': 'mp4'
    }

    clean_data = clean_video_data(data)

    assert clean_data == {
        'title': 'video',
        'url': 'http://test.it/video.mp4',
        'ext': 'mp4'
    }


@pytest.mark.parametrize('url, domain_name', [
    ('http://audycje.tokfm.pl/podcast/', 'tokfm.pl'),
    ('https://vod.tvp.pl/video/', 'tvp.pl'),
    ('http://www.rmf24.pl/tylko-w-rmf24/', 'rmf24.pl'),

])
def test_extracting_domain_name(url, domain_name):
    assert get_domain_name(url) == domain_name


def test_extracting_domain_name_with_wrong_url_raises_error():
    url = 'http://google'
    with pytest.raises(WrongUrlError):
        get_domain_name(url)


@pytest.fixture()
def stdout():
    old_stdout = sys.stdout
    result = StringIO()
    sys.stdout = result

    yield result

    sys.stdout = old_stdout


def test_supressing_stdout(stdout):
    with suppress_stdout():
        print('Test print')
    assert stdout.getvalue() == ''
