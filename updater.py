import os
from datetime import (
    datetime,
    timedelta,
)
from time import sleep

from dotenv import load_dotenv
from notion_client import Client

import log
from title import get_title

load_dotenv()

logger = log.init()


WEEKLY_ID = "0ba2699e66a64826b0dc32563ae1f41e"
twenty_twenty_three_id = "b1a820decce443c795f7157f77bd7698"


class Updater:
    TEMPLATE_NAME = "[Template] Week N, Month, Year (MM/DD—MM/DD) (1)"
    NEXT_WEEK_TEMPLATE = "{{next}}"
    INTERVAL = int(os.environ.get("INTERVAL_IN_SEC", "60"))

    def __init__(self, watch_page_id: str) -> None:
        self.watch_page_id = watch_page_id

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
        page_ids = self._detect_changes(self.watch_page_id)
        for page_id, new_title in page_ids.items():
            self._update_title(page_id, new_title)

    def _detect_changes(self, parent_child_id: str):
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
    watcher = Updater(twenty_twenty_three_id)
    watcher.watch()


if __name__ == "__main__":
    main()
