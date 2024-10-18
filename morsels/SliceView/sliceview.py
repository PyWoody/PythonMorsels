class SliceView:

    def __init__(self, iterable, start=None, stop=None, step=None):
        self.iterable = iterable
        self.slice = slice(start, stop, step)

    def __len__(self):
        count = 0
        for _ in self:
            count += 1
        return count

    def __getitem__(self, index):
        if isinstance(index, slice):
            return SliceView(self.iterable[self.slice][index])
        else:
            try:
                return self.iterable[self.slice][index]
            except Exception:
                return list(self.iterable)[self.slice][index]
