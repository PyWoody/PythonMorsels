class SequenceZip:

    def __init__(self, *iterables):
        self.iterables = iterables
        self.len = min((len(i) for i in self.iterables), default=0)

    def __repr__(self):
        cls = self.__class__.__name__
        return f'{cls}({", ".join(repr(i) for i in self.iterables)})'

    def __iter__(self):
        iterables = [list(i)[:self.len] for i in self.iterables]
        for index in range(self.len):
            yield tuple(i[index] for i in iterables)

    def __len__(self):
        return self.len

    def __eq__(self, other):
        if isinstance(other, SequenceZip):
            return list(self) == list(other)
        for i, v in enumerate(self.iterables):
            try:
                if other[i] != v:
                    return False
            except IndexError:
                return False
        return True

    def __getitem__(self, index):
        if self.len == 0:
            raise IndexError
        if isinstance(index, int):
            if index > self.len or index * -1 > self.len:
                raise IndexError
            if index < 0:
                return tuple(i[:self.len][index] for i in self.iterables)
            return tuple(i[index] for i in self.iterables)
        if isinstance(index, slice):
            sequence = self.build_indexes(index)
            output = []
            for i in range(len(sequence[0])):
                loop = []
                for seq in sequence:
                    loop.append(seq[i])
                output.append(loop)
            return SequenceZip(*output)


    def build_indexes(self, index):
        iterables = [iter(i[:self.len][index]) for i in self.iterables]
        output = []
        while True:
            try:
                for _ in range(len(iterables)):
                    output.append(list(next(i) for i in iterables))
            except RuntimeError:
                break
        return output
