class PiecewiseRange:

    def __init__(self, str_range):
        self.ranges = []
        for str_range in str_range.split(','):
            if '-' in str_range:
                start, stop = str_range.split('-')
                self.ranges.append((int(start), int(stop) + 1))
            else:
                self.ranges.append((int(str_range), int(str_range) + 1))
        self.ranges.sort(key=lambda x: x[0])

    def __repr__(self):
        cls = self.__class__.__name__
        output = []
        index = 0
        start = self.ranges[index]
        while True:
            if index + 1 < len(self.ranges) and self.ranges[index][1] <= self.ranges[index + 1][0]:
                index += 1
                continue
            if start[0] == self.ranges[index][1]:
                output.append(str(start[0]))
            else:
                output.append(
                    '-'.join([str(start[0]), str(self.ranges[index][1] - 1)])
                )
            if index + 1 >= len(self.ranges):
                break
            index += 1
            start = self.ranges[index]
        args = ', '.join(output)
        return f'{cls}({args!r})'

    def __eq__(self, other):
        if isinstance(other, PiecewiseRange):
            return repr(self) == repr(other)
        return NotImplemented

    def __iter__(self):
        for r in self.ranges:
            yield from range(*r)

    def __len__(self):
        return sum(stop - start for start, stop in self.ranges)

    def __getitem__(self, index):
        return list(self)[index]
