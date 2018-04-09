import pytest
from directory_inspect import get_files, find_directory
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))


@pytest.fixture
def files():
    return get_files(BASE_DIR+"/fixtures")


def test_root_on_the_files_list(files):
    assert ('folders' and 'files') in files['course']
    assert ("chapter_1" and "chapter_2" and "chapter_3") in files['course']['folders']
    assert files['course']['files'] == []


def test_chapter_1_on_the_files_list(files):
    assert ('folders' and 'files') in files['course']['folders']['chapter_1']
    assert files['course']['folders']['chapter_1']['folders'] == {}
    assert files['course']['folders']['chapter_1']['files'] == ["example.mp4"]


def test_chapter_2_on_the_files_list(files):
    assert ('folders' and 'files') in files['course']['folders']['chapter_2']
    assert "folder" in files['course']['folders']['chapter_2']['folders']
    assert files['course']['folders']['chapter_2']['files'] == ["example_2.mp4"]

    assert ('folders' and 'files') in files['course']['folders']['chapter_2']['folders']['folder']
    assert files['course']['folders']['chapter_2']['folders']['folder']['folders'] == {}
    assert files['course']['folders']['chapter_2']['folders']['folder']['files'] == ["example_2_1.mp4"]


def test_chapter_3_on_the_files_list(files):
    chapter_3_files = ("image_example.png" and "example_3.mp4" and "text_example.pdf")
    assert ('folders' and 'files') in files['course']['folders']['chapter_3']
    assert files['course']['folders']['chapter_3']['folders'] == {}
    assert chapter_3_files in files['course']['folders']['chapter_3']['files']


@pytest.mark.parametrize("path", ["/fixtures/", "/fixtures"])
def test_slash_at_end_path(path):
    files_and_folders = get_files(BASE_DIR+path)
    assert "course" in files_and_folders.keys()


def test_find_directory_by_path_url(files):
    folders, files = find_directory("course/chapter_2/folder", files)
    assert folders == {}
    assert files == ["example_2_1.mp4"]