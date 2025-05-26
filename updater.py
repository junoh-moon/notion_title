import os
from datetime import (
    datetime,
    timedelta,
)
from time import sleep
from typing import (
    Callable,
    Iterable,
    TypeVar,
)

from dotenv import load_dotenv
from notion_client import Client

import log
from title import get_title

load_dotenv()

logger = log.init()


PAGE_ID_MAPPING = {
    # "Weekly progress home": "0ba2699e66a64826b0dc32563ae1f41e",
    # "2023": "b1a820decce443c795f7157f77bd7698",
    # "2024": "2ba0c3f7a50a43d680b51ce1a59f423f",
    "2025": "166e95c5c8e580c084dffefd91d48b59",
}

T = TypeVar("T")
U = TypeVar("U")


def flatmap(func: Callable[[T], dict[str, U]], iter: Iterable[T]) -> dict[str, U]:
    acc: dict[str, U] = {}
    for arg in iter:
        acc |= func(arg)
    return acc


class Updater:
    TEMPLATE_NAME = "[Template] Week N, Month, Year (MM/DD—MM/DD) (1)"
    NEXT_WEEK_TEMPLATE = "{{next}}"
    INTERVAL = int(os.environ.get("INTERVAL_IN_SEC", "60"))

    def __init__(self, *watch_page_ids: str) -> None:
        self.watch_page_ids = list(watch_page_ids)

        token = os.environ["NOTION_TOKEN"]
        self.notion = Client(auth=token)

        self.new_title = get_title(today=datetime.now().date())

        logger.info(f"{self.new_title=}, {self.TEMPLATE_NAME=}")
        return

    def watch(self):
        while True:
            self.update()
            sleep(self.INTERVAL)

    def update(self):
        page_ids = flatmap(self._detect_changes, self.watch_page_ids)
        for page_id, new_title in page_ids.items():
            self._update_title(page_id, new_title)

    def _detect_changes(self, parent_child_id: str) -> dict[str, str]:
        page_title_mapping = dict()
        children = self.notion.blocks.children.list(parent_child_id)
        logger.info(children)
        for child in children["results"]:  # type: ignore
            logger.debug(child)
            if child["type"] != "child_page":
                continue
            title: str = child["child_page"]["title"]
            new_title = {
                True: None,
                title == self.TEMPLATE_NAME: get_title(datetime.now().date()),
                title.lower()
                == self.NEXT_WEEK_TEMPLATE: get_title(
                    (datetime.now() + timedelta(days=7)).date()
                ),
            }[True]
            if new_title is None:
                continue
            child_id = child["id"]
            page_title_mapping[child_id] = new_title

        logger.info(f"{page_title_mapping=}")
        return page_title_mapping

    def _update_title(self, page_id: str, new_title: str):
        body = self.notion.pages.retrieve(page_id)
        logger.info(f"Previous: {body}")

        body["properties"]["title"]["title"][0]["text"][
            "content"
        ] = new_title  # type: ignore

        resp = self.notion.pages.update(page_id, **body)  # type: ignore
        logger.info(f"After: {resp}")

        return resp["properties"]["title"]["title"][0]["text"]["content"]


def main():
    watcher = Updater(*PAGE_ID_MAPPING.values())
    watcher.watch()


if __name__ == "__main__":
    main()
