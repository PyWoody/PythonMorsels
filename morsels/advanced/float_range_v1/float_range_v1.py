import itertools


class float_range:

    def __init__(self, start, stop=None, step=1.0):
        if float(step) == 0.0:
            raise ValueError
        if stop is None:
            self.start = 0.0
            self.stop = float(start)
        else:
            self.start = float(start)
            self.stop = float(stop)
        self.step = float(step)
        self.output = None

    def __repr__(self):
        cls = self.__class__.__name__
        start = int(self.start) if self.start.is_integer() else self.start
        stop = int(self.stop) if self.stop.is_integer() else self.stop
        step = int(self.step) if self.step.is_integer() else self.step
        return f'{cls}({start}, {stop}, {step})'

    def __eq__(self, other):
        if isinstance(other, float_range):
            if other.step.is_integer():
                s_start = int(self.start) if self.start.is_integer() else int(self.start) + 1
                s_stop = int(self.stop) if self.stop.is_integer() else int(self.stop) + 1
                s_step = int(self.step) if self.step.is_integer() else int(self.step) + 1

                o_start = int(other.start) if other.start.is_integer() else int(other.start) + 1
                o_stop = int(other.stop) if other.stop.is_integer() else int(other.stop) + 1
                o_step = int(other.step) if other.step.is_integer() else int(other.step) + 1
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
                    self.start == other.start,
                    self.stop == other.stop,
                    self.step == other.step,
                ]
            ):
                return True
            return list(self) == list(other)
        if isinstance(other, range):
            return [int(i) for i in self] == list(other)
        return list(self) == other

    def __iter__(self):
        if self.output:
            yield from self.output
            return
        if self.start == self.stop:
            return
        if self.step > 0.0:
            positive = True
            if self.start > self.stop:
                return
        else:
            positive = False
            if self.stop > self.start:
                return
        output = []
        curr = self.start
        while compare(curr, self.stop, positive=positive):
            yield curr
            output.append(curr)
            curr += self.step
        self.output = output

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

    def __len__(self):
        if self.output:
            return len(self.output)
        count = 0
        for _ in self:
            count += 1
        return count
    

def compare(left, right, positive=True):
    if positive:
        if left < right:
            return True
        return False
    if left > right:
        return True
    return False
