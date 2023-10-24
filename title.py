import calendar
import datetime
from argparse import (
    ArgumentParser,
    Namespace,
)
from datetime import date

from requests import post

import log

logger = log.init()


def get_month_and_week_number(date: datetime.date) -> tuple[str, int]:
    """
    Given a date, it firstly gets a range of dates from Monday to Sunday that includes the given date.
    Second, calculates the month and week number of Wednesday.
    Returns a tuple of month name and week number which are already calculated.
    """  # noqa
    # Calculate the date range from Monday to Sunday that includes the given date
    start_date = date - datetime.timedelta(days=date.weekday())

    # Calculate the month and week number of Wednesday in the date range
    wednesday = start_date + datetime.timedelta(days=2)
    week_number = (wednesday.day - 1) // 7 + 1

    # Get the month name based on the month number
    month_name = calendar.month_name[wednesday.month]

    return month_name, week_number


def get_week_range(date: datetime.date) -> tuple[str, str]:
    """
    Given a date, calculates the date range from Monday to Sunday that includes the date.
    Returns a tuple of Monday and Sunday dates in the format "mm/dd".
    """  # noqa
    # Calculate the date range from Monday to Sunday that includes the given date
    start_date = date - datetime.timedelta(days=date.weekday())
    end_date = start_date + datetime.timedelta(days=6)

    # Format the dates as "mm/dd"
    start_date_str = start_date.strftime("%m/%d")
    end_date_str = end_date.strftime("%m/%d")

    return start_date_str, end_date_str


def get_title(today: date):
    month, week_number = get_month_and_week_number(today)
    monday, sunday = get_week_range(today)

    title = f"Week {week_number}, {month}, {today.year} ({monday}—{sunday})"
    return title


def main(args: Namespace):
    title = get_title(args.date)
    logger.info(title)

    if args.notify:
        post("https://ntfy.sixtyfive.me/notion_title", data=title.encode())

    return


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("date", type=date.fromisoformat)
    parser.add_argument("--notify", action="store_true")
    main(parser.parse_args())
