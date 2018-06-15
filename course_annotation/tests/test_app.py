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
