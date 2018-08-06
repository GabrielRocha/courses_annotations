import os
from collections import defaultdict

import pytest

import directory_inspect

BASE_DIR = f'{os.path.dirname(os.path.abspath(__file__))}/fixtures/'
directory_inspect.COURSE_PATH = BASE_DIR


@pytest.fixture
def files():
    return directory_inspect.get_files(f'{BASE_DIR}/folder_tree')


def test_root_on_the_files_list(files):
    assert ('folders' and 'files') in files['course']
    assert ("chapter_1" and "chapter_2" and "chapter_3") in files['course']['folders']
    assert files['course']['files'] == defaultdict()


def test_chapter_1_on_the_files_list(files):
    expected = {'example': {'video': 'example.mp4', "annotation": "example.html"}}
    assert ('folders' and 'files') in files['course']['folders']['chapter_1']
    assert files['course']['folders']['chapter_1']['folders'] == {}
    assert files['course']['folders']['chapter_1']['files'] == expected


def test_chapter_2_on_the_files_list(files):
    assert ('folders' and 'files') in files['course']['folders']['chapter_2']
    assert "folder" in files['course']['folders']['chapter_2']['folders']
    assert files['course']['folders']['chapter_2']['files'] == {'example_2': {'video': 'example_2.mp4'}}


def test_files_on_chapter_2_under_more_one_level(files):
    expected = {'example_2_1': {'video': 'example_2_1.mp4'}}
    assert ('folders' and 'files') in files['course']['folders']['chapter_2']['folders']['folder']
    assert files['course']['folders']['chapter_2']['folders']['folder']['folders'] == {}
    assert files['course']['folders']['chapter_2']['folders']['folder']['files'] == expected


def test_chapter_3_on_the_files_list(files):
    assert ('folders' and 'files') in files['course']['folders']['chapter_3']
    assert files['course']['folders']['chapter_3']['folders'] == {}
    assert files['course']['folders']['chapter_3']['files'] == {'example_3': {'video': 'example_3.mp4'}}


@pytest.mark.parametrize("path", ["/folder_tree/", "/folder_tree"])
def test_slash_at_end_path(path):
    directory_inspect.CREATE_ANNOTATION = False
    files_and_folders = directory_inspect.get_files(BASE_DIR+path)
    assert "course" in files_and_folders.keys()


def test_group_by_type():
    directory_inspect.CREATE_ANNOTATION = False
    files = ['example_3.mp4', 'image_example.png', 'text_example.pdf', 'example_3.html']
    expected = {"example_3": {"video": "example_3.mp4", "annotation": "example_3.html"}}
    assert directory_inspect.group_by_type(files) == expected


def test_find_directory_by_path_url(files):
    folders, files = directory_inspect.find_directory("course/chapter_2/folder", files)
    assert folders == {}
    assert files == {'example_2_1': {'video': 'example_2_1.mp4'}}
