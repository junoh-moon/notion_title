import datetime

from title import (
    get_month_and_week_number,
    get_title,
    get_week_range,
)


def test_get_month_and_week_number():
    date = datetime.date(2023, 2, 27)
    assert get_month_and_week_number(date) == ("March", 1)

    date = datetime.date(2023, 3, 5)
    assert get_month_and_week_number(date) == ("March", 1)

    date = datetime.date(2023, 3, 6)
    assert get_month_and_week_number(date) == ("March", 2)

    date = datetime.date(2023, 3, 13)
    assert get_month_and_week_number(date) == ("March", 3)

    date = datetime.date(2023, 3, 18)
    assert get_month_and_week_number(date) == ("March", 3)

    date = datetime.date(2023, 3, 20)
    assert get_month_and_week_number(date) == ("March", 4)

    date = datetime.date(2023, 3, 28)
    assert get_month_and_week_number(date) == ("March", 5)

    date = datetime.date(2023, 5, 1)
    assert get_month_and_week_number(date) == ("May", 1)


def test_get_week_range():
    date = datetime.date(2023, 3, 18)
    start_date, end_date = get_week_range(date)
    assert start_date == "03/13"
    assert end_date == "03/19"

    date = datetime.date(2022, 11, 2)
    start_date, end_date = get_week_range(date)
    assert start_date == "10/31"
    assert end_date == "11/06"

    date = datetime.date(2024, 12, 31)
    start_date, end_date = get_week_range(date)
    assert start_date == "12/30"
    assert end_date == "01/05"

    date = datetime.date(2021, 1, 1)
    start_date, end_date = get_week_range(date)
    assert start_date == "12/28"
    assert end_date == "01/03"


def test_get_title():
    expected = "Week 3, April, 2023 (04/17—04/23)"
    date = datetime.date(2023, 4, 17)
    actual = get_title(date)
    assert actual == expected
