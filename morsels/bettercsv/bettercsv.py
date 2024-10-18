import csv


class FancyReader:

    def __init__(self, lines, *, fieldnames=None):
        self.__line_num = 0
        self.lines = iter(lines)
        if fieldnames is None:
            fieldnames = next(csv.reader([next(self.lines)]))
            self.__line_num += 1
        self.header = list(fieldnames)

    def __iter__(self):
        while True:
            try:
                yield next(self)
            except StopIteration:
                break

    def __next__(self):
        line = csv.reader([next(self.lines)])
        data = {self.header[i]: v.strip() for i, v in enumerate(next(line))}
        self.__line_num += 1
        return Row(data)

    @property
    def line_num(self):
        return self.__line_num



class Row:

    def __init__(self, data):
        self.data = dict(data)

    def __repr__(self):
        cls = self.__class__.__name__
        kwargs = ', '.join(
            '='.join((k, repr(v))) for k, v in self.data.items()
        )
        return f'{cls}({kwargs})'

    def __iter__(self):
        yield from self.data.values()

    def __getitem__(self, key):
        return self.data[key]

    def __getattr__(self, key):
        return self.data[key]
