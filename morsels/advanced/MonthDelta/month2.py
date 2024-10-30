from datetime import datetime


class Month:

    def __init__(self, year, month):
        if month < 1 or month > 12:
            raise ValueError
        self.year = int(year)
        self.month = int(month)

    def __repr__(self):
        cls = self.__class__.__name__
        return f'{cls}({repr(self.year)}, {repr(self.month)})'

    def __eq__(self, other):
        if isinstance(other, type(self)):
            return self.year == other.year and self.month == other.month
        return NotImplemented

    def __format__(self, spec):
        return datetime(self.year, self.month, 1).strftime(spec)

    def __add__(self, other):
        if not isinstance(other, MonthDelta):
            raise TypeError
        year = self.year
        month = self.month + other.months
        if month > 12:
            add_years, month = divmod(month, 12)
            if month == 0:
                add_years -= 1
                month = 12
            year += add_years
        return Month(year, month)

    def __sub__(self, other):
        year = self.year
        if isinstance(other, MonthDelta):
            month = self.month - other.months
            while month < 1:
                year -= 1
                month += 12
            return Month(year, month)
        elif isinstance(other, type(self)):
            month = self.month - other.month
            while month < 1:
                year -= 1
                month += 12
            year = year - other.year
            return MonthDelta(year * 12 + month)
        raise TypeError


class MonthDelta:

    def __init__(self, months):
        self.months = int(months)

    def __repr__(self):
        cls = self.__class__.__name__
        return f'{cls}({repr(self.months)})'

    def __eq__(self, other):
        if isinstance(other, type(self)):
            return self.months == other.months
        return NotImplemented

    def __add__(self, other):
        year = 0
        if isinstance(other, Month):
            year = other.year
            month = self.months + other.month
            if month > 12:
                year += 1
                month -= 12
            return Month(year, month)
        elif isinstance(other, type(self)):
            return MonthDelta(self.months + other.months)
        raise TypeError

    def __sub__(self, other):
        if not isinstance(other, type(self)):
            raise TypeError
        return MonthDelta(self.months - other.months)

    def __mul__(self, other):
        if isinstance(other, type(self)):
            raise TypeError
        elif isinstance(other, int):
            return MonthDelta(self.months * other)
        return NotImplemented

    __rmul__ = __mul__

    def __truediv__(self, other):
        if isinstance(other, type(self)):
            return self.months / other.months
        elif isinstance(other, int):
            return MonthDelta(self.months / other)
        return NotImplemented

    __rtruediv__ = __truediv__

    def __floordiv__(self, other):
        if isinstance(other, type(self)):
            return self.months // other.months
        elif isinstance(other, int):
            return MonthDelta(self.months // other)
        return NotImplemented

    __rfloordiv__ = __floordiv__

    def __mod__(self, other):
        if isinstance(other, type(self)):
            return self.months % other.months
        elif isinstance(other, int):
            return MonthDelta(self.months % other)
        return NotImplemented

    __rmod__ = __mod__

    def __neg__(self):
        return MonthDelta(self.months * -1)
