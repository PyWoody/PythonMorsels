import itertools

from calendar import Calendar
from datetime import datetime
from functools import total_ordering


@total_ordering
class Month:

    __slots__ = ('__year', '__month', '__first_day', '__last_day')

    def __init__(self, year, month):
        self.__year = int(year)
        self.__month = int(month)
        if self.__month > 12:
            raise Exception
        self.__first_day = None
        self.__last_day = None

    def __hash__(self):
        return hash((self.year, self.month))

    def __repr__(self):
        cls = self.__class__.__name__
        return f'{cls}({self.year}, {self.month})'

    def __str__(self):
        return f'{self.year}-{str(self.month).zfill(2)}'

    def __eq__(self, other):
        if isinstance(other, type(self)):
            return hash(other) == hash(self)
        return NotImplemented

    def __lt__(self, other):
        if isinstance(other, type(self)):
            if self.year < other.year:
                return True
            elif self.year == other.year and self.month < other.month:
                return True
            return False
        return NotImplemented

    @classmethod
    def from_date(cls, date):
        return cls(date.year, date.month)

    @property
    def year(self):
        return self.__year

    @property
    def month(self):
        return self.__month

    @property
    def first_day(self):
        if self.__first_day is None:
            for date in Calendar().itermonthdates(self.year, self.month):
                if date.month == self.month:
                    self.__first_day = date
                    break
        return self.__first_day

    @property
    def last_day(self):
        if self.__last_day is None:
            dates = itertools.dropwhile(
                lambda x: x.month != self.month, 
                Calendar().itermonthdates(self.year, self.month)
            )
            prev = None
            for date in dates:
                if date.month != self.month:
                    self.__last_day = prev
                    break
                prev = date
        return self.__last_day

    def strftime(self, ftime):
        return datetime(self.year, self.month, 1).strftime(ftime)
