from contextlib import contextmanager
from decimal import Decimal
from numbers import Number



class Comparator:

    default = None

    def __init__(self, value, delta=None):
        self.value = value
        if delta is None and self.default is None:
            self.delta = 0.0000001
        elif delta:
            self.delta = delta
        else:
            self.delta = self.default

    def __repr__(self):
        cls = self.__class__.__name__
        return f'{cls}({self.value!r}, delta={self.delta!r})'

    def __eq__(self, other):
        if isinstance(other, type(self)):
            other_value = other.value
            delta = max(self.delta, other.delta)
        elif isinstance(other, Number):
            other_value = other
            delta = self.delta
        else:
            return NotImplemented
        value = self.value if self.value > 0 else self.value * - 1
        other_value = other_value if other_value > 0 else other_value * - 1
        if self.value == other_value:
            return True
        gt = float(Decimal(value) + Decimal(delta))
        lt = float(Decimal(value) - Decimal(delta))
        return lt <= other_value <= gt

    def __add__(self, other):
        if isinstance(other, type(self)):
            return Comparator(
                self.value + other.value,
                delta=max(self.delta, other.delta),
            )
        elif isinstance(other, Number):
            return Comparator(self.value + other, delta=self.delta)
        return NotImplemented

    __radd__ = __add__

    def __sub__(self, other):
        if isinstance(other, type(self)):
            return Comparator(
                self.value - other.value,
                delta=max(self.delta, other.delta),
            )
        elif isinstance(other, Number):
            return Comparator(self.value - other, delta=self.delta)
        return NotImplemented

    __rsub__ = __sub__

    def __float__(self):
        return float(self.value)

    def __int__(self):
        return int(self.value)

    @classmethod
    @contextmanager
    def default_delta(cls, delta):
        try:
            cls.default = delta
            yield
        finally:
            cls.default = None
