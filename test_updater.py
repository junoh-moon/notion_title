import pytest
from freezegun import freeze_time
from pytest_mock import MockerFixture

from mock.pages import (
    PAGE,
    PAGES,
    UPDATED_PAGE,
)
from updater import Updater


@pytest.fixture
def setup_update(mocker: MockerFixture):
    class MockClient:
        def __init__(self, *args, **kwargs):
            pass

        class Blocks:
            class Children:
                def list(self, *args, **kwargs):
                    return PAGES

            children = Children()

        class Pages:
            def retrieve(self, *args, **kwargs):
                return PAGE

            def update(self, *args, **kwargs):
                return UPDATED_PAGE

        pages = Pages()
        blocks = Blocks()

    mocker.patch("updater.Client", MockClient)
    return


def test_update_title(setup_update: None):
    expected = "Week 4, October, 2023 (10/23—10/29)"

    updater = Updater("asdf")
    assert updater._update_title("hello_world", expected) == expected

    return


@freeze_time("2023-10-25")
def test_detect_changes(setup_update: None):
    updater = Updater("asdf")
    actual = updater._detect_changes("fake_id")
    expected = {
        "7660867e-e9bf-449e-9f72-9e8314a7dc3c": "Week 4, October, 2023 (10/23—10/29)",
        "8d04578a-5371-4469-859a-e7aad9d5cf3d": "Week 1, November, 2023 (10/30—11/05)",
    }
    assert actual == expected
    return
