class SequenceZip:

    def __init__(self, *sequences):
        self.sequences = sequences
        self.len = min((len(i) for i in self.sequences), default=0)

    def __repr__(self):
        cls = self.__class__.__name__
        return f'{cls}({", ".join(repr(i) for i in self.sequences)})'

    def __len__(self):
        return self.len

    def __iter__(self):
        sequences = [iter(i) for i in self.sequences]
        for index in range(self.len):
            yield tuple(next(i) for i in sequences)

    def __eq__(self, other):
        if isinstance(other, type(self)):
            return tuple(self) == tuple(other)
        return NotImplemented

    def __ne__(self, other):
        if isinstance(other, type(self)):
            return tuple(self) != tuple(other)
        return NotImplemented

    def __getitem__(self, index):
        if self.len == 0:
            raise IndexError
        if isinstance(index, int):
            if index > self.len or index * -1 > self.len:
                raise IndexError
            if index < 0:
                return tuple(i[:self.len][index] for i in self.sequences)
            return tuple(i[index] for i in self.sequences)
        if isinstance(index, slice):
            sequence = self.build_indexes(index)
            output = []
            for i in range(len(sequence[0])):
                loop = []
                for seq in sequence:
                    loop.append(seq[i])
                output.append(loop)
            return SequenceZip(*output)

    def __setitem__(self, key, values):
        if len(values) != len(self.sequences):
            raise ValueError
        if key > self.len or key * -1 > self.len:
            raise IndexError
        if key < 0:
            key_slice = slice(None, None, key)
            key, *_ = key_slice.indices(self.len)
        for val, seq in zip(values, self.sequences):
            seq[key] = val

    def __delitem__(self, key):
        if key > self.len or key * -1 >= self.len:
            raise IndexError
        if key < 0:
            key_slice = slice(None, None, key)
            key, *_ = key_slice.indices(self.len)
            key -= 1
        for seq in self.sequences:
            del seq[key]

    def build_indexes(self, index):
        iterables = [iter(i[:self.len][index]) for i in self.sequences]
        output = []
        while True:
            try:
                for _ in range(len(iterables)):
                    output.append(list(next(i) for i in iterables))
            except RuntimeError:
                break
        return output

    def append(self, values):
        if len(values) != len(self.sequences):
            raise ValueError
        for val, seq in zip(values, self.sequences):
            if len(seq) > self.len:
                seq[self.len] = val
            else:
                seq.append(val)
        self.len = min((len(i) for i in self.sequences), default=0)

    def insert(self, index, values):
        if len(values) != len(self.sequences):
            raise ValueError
        if index > self.len or index * -1 > self.len:
            raise IndexError
        for val, seq in zip(values, self.sequences):
            seq.insert(index, val)
        self.len = min((len(i) for i in self.sequences), default=0)
