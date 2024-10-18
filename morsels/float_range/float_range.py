import itertools


class float_range:

    def __init__(self, start, stop=None, step=1):
        if float(step) == 0.0:
            raise ValueError
        if stop is None:
            self.start = 0
            self.stop = start
            self.step = 1
        else:
            self.start = start
            self.stop = stop
            self.step = step
        self.internal_list = []

    def __repr__(self):
        cls = self.__class__.__name__
        return f'{cls}({self.start!r}, {self.stop!r}, {self.step!r})'

    def __eq__(self, other):
        if isinstance(other, type(self)):
            if float(other.step).is_integer():
                s_start = int(self.start) if float(self.start).is_integer() else int(self.start) + 1
                s_stop = int(self.stop) if float(self.stop).is_integer() else int(self.stop) + 1
                s_step = int(self.step) if float(self.step).is_integer() else int(self.step) + 1

                o_start = int(other.start) if float(other.start).is_integer() else int(other.start) + 1
                o_stop = int(other.stop) if float(other.stop).is_integer() else int(other.stop) + 1
                o_step = int(other.step) if float(other.step).is_integer() else int(other.step) + 1
                if all(
                    [
                        s_start == o_start,
                        s_step == o_step,
                        s_stop == o_stop,
                    ]
                ):
                    return True
            elif all(
                [
                    float(self.start) == float(other.start),
                    float(self.stop) == float(other.stop),
                    float(self.step) == float(other.step),
                ]
            ):
                return True
            return list(self) == list(other)
        elif isinstance(other, range):
            return [int(i) for i in self] == list(other)
        return NotImplemented

    def __iter__(self):
        if self.start == self.stop:
            return
        if self.internal_list:
            yield from self.internal_list
            return
        i_list = []
        head = self.start
        if self.step < 0:
            while head > self.stop:
                yield head
                i_list.append(head)
                head += self.step
        else:
            while head < self.stop:
                yield head
                i_list.append(head)
                head += self.step
        self.internal_list = i_list

    def __len__(self):
        if self.internal_list:
            return len(self.internal_list)
        count = 0
        for _ in self:
            count += 1
        return count

    def __getitem__(self, index):
        if isinstance(index, int):
            if index > 0:
                try:
                    return next(itertools.islice(self, index, index + 1))
                except StopIteration:
                    raise IndexError
            else:
                return list(self)[index]
        elif isinstance(index, slice):
            try:
                start, stop = index.start, index.stop
                if start is not None and start < 0:
                    return list(self)[index]
                elif stop is not None and stop < 0:
                    return list(self)[index]
                elif stop is None and start is None:
                    return list(self)[index]
                return list(itertools.islice(self, start, stop))
            except StopIteration:
                raise IndexError
        raise TypeError
