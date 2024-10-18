import csv


class FancyReader:

    def __init__(self, lines, delimiter=',', fieldnames=None):
        self.reader = csv.reader(lines, delimiter=delimiter)
        self.__fieldnames = list(fieldnames) if fieldnames else None

    def __iter__(self):
        fieldnames = self.fieldnames
        for row in self.reader:
            Row = make_row(tuple(fieldnames))
            yield Row(row, header=fieldnames)

    def __next__(self):
        return next(iter(self))

    @property
    def line_num(self):
        return self.reader.line_num

    @property
    def fieldnames(self):
        if self.__fieldnames is None:
            self.__fieldnames = list(next(self.reader))
        return self.__fieldnames


def make_row(slots):

    class Row:

        __slots__ = slots

        def __init__(self, row, *, header):
            for name, value in zip(header, row):
                super().__setattr__(name, value)

        def __iter__(self):
            for attr in self.__slots__:
                yield getattr(self, attr)

        def __repr__(self):
            cls = self.__class__.__name__
            args = (
                '='.join((attr, repr(getattr(self, attr))))
                for attr in self.__slots__
            )
            return f'{cls}({", ".join(args)})'

    return Row
