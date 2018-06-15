import pytest

import app as flask_application
from .fixtures.helper import COURSE_STRUCTURE


@pytest.fixture
def app():
    flask_application.COUSE_STRUCTURE = COURSE_STRUCTURE
    return flask_application.app


@pytest.mark.parametrize('tag', [
    '<a href="/chapter/chapter_1/">chapter_1</a>',
    '<a href="/chapter/chapter_2/">chapter_2</a>',
    '<a href="/chapter/chapter_3/">chapter_3</a>'
])
def test_index(client, tag):
    response = client.get('/')
    assert tag in response.data.decode()


@pytest.mark.parametrize('url, file, annotation', [
    (
        '/chapter/chapter_1/',
        'link="chapter_1/example.html"',
        'source src="/file/chapter_1/example.mp4"'
    ),
    (
        '/chapter/chapter_2/',
        '',
        'source src="/file/chapter_2/example_2.mp4"'
    ),
    (
        '/chapter/chapter_3/',
        '',
        'source src="/file/chapter_3/example_3.mp4"'
    ),
])
def test_folder_videos_and_annotations(client, url, file, annotation):
    response = client.get(url)
    assert file in response.data.decode()
    assert annotation in response.data.decode()


def test_second_level_folder(client):
    response = client.get('/chapter/chapter_2/')
    tag = '<a href="/chapter/chapter_2/folder/">folder</a>'
    assert tag in response.data.decode()


def test_videos_in_second_level_folder(client):
    response = client.get('/chapter/chapter_2/folder/')
    video = 'source src="/file/chapter_2/folder/example_2_1.mp4"'
    assert video in response.data.decode()
