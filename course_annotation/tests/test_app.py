import re

import pytest

import app as flask_application


def request(client, url):
    response = client.get(url)
    return re.sub(r'\n|  ', '', response.data.decode())


@pytest.fixture
def app(course_structure):
    flask_application.COURSE_STRUCTURE = course_structure
    return flask_application.app


@pytest.mark.parametrize('tag', [
    '<a class="title" href="/chapter/chapter_1">chapter_1</a>',
    '<a class="title" href="/chapter/chapter_2">chapter_2</a>',
    '<a href="/chapter/chapter_3">chapter_3</a>'
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
    html = request(client, url)
    assert file in html
    assert annotation in html


def test_second_level_folder(client):
    tag = '<a href="/chapter/chapter_2/folder">folder</a>'
    html = request(client, '/chapter/chapter_2/')
    assert tag in html


def test_videos_in_second_level_folder(client):
    video = '<source src="/file/chapter_2/folder/example_2_1.mp4" type="video/mp4">'
    button = '<button class="create_annotation btn btn-success"file="chapter_2/' \
             'folder/example_2_1"><b>Create Annotation</b></button>'
    html = request(client, '/chapter/chapter_2/folder/')
    assert video in html
    assert button in html
