import calendar
from enum import IntEnum


class Weekday(IntEnum):
    MONDAY = 0
    TUESDAY = 1
    WEDNESDAY = 2
    THURSDAY = 3
    FRIDAY = 4
    SATURDAY = 5
    SUNDAY = 6


def meetup_date(year, month, nth=4, weekday=Weekday.THURSDAY):
    # Fourth Thursday except holidays
    weekday = int(weekday)
    days = [
        i for i in calendar.Calendar().itermonthdates(year, month)
        if i.month == month and i.weekday() == weekday
    ]
    if nth < 0:
        return days[nth]
    return days[nth-1]


print(meetup_date(2023, 3))
