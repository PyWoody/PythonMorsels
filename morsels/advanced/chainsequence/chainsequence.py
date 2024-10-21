from typing import Sequence


class ChainSequence:

    def __init__(self, *sequences):
        self.sequences = list(sequences)

    def __repr__(self):
        cls = self.__class__.__name__
        return f'{cls}({", ".join(repr(i) for i in self.sequences)})'

    def __iter__(self):
        for seq in self.sequences:
            if isinstance(seq, Sequence):
                yield from seq
            else:
                yield from list(seq)

    def __len__(self):
        return sum(len(i) for i in self.sequences)

    def __getitem__(self, index):
        if isinstance(index, slice):
            start, stop, step = index.start, index.stop, index.step
            return SliceView(self, start, stop, step)
        return list(self)[index]

    def __add__(self, item):
        sequences = self.sequences[:]
        if isinstance(item, type(self)):
            sequences.extend(item.sequences)
        else:
            sequences.append(item)
        return type(self)(*sequences)

    def __iadd__(self, item):
        if isinstance(item, type(self)):
            self.sequences.extend(item.sequences)
        else:
            self.sequences.append(item)
        return self

    def append(self, item):
        self.sequences.append(item)


class SliceView(Sequence):

    def __init__(self, sequence, start=None, stop=None, step=None):
        start, stop, step = slice(start, stop, step).indices(len(sequence))
        self.range = range(start, stop, step)
        self.sequence = sequence

    def __len__(self):
        return len(self.range)

    def __getitem__(self, index):
        if not isinstance(index, slice):
            return list(self.sequence)[self.range[index]]
        else:
            return SliceView(self, index.start, index.stop, index.step)
