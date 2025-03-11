import itertools


class fancy:

    def __init__(self, iterable=None, restarable=False):
        self.iterables = [iter(iterable)] if iterable is not None else []
        self.results = []
        self.restarable = bool(restarable)

    def __iter__(self):
        if self.iterables:
            while self.iterables:
                try:
                    result = next(self.iterables[0])
                    self.results.append(result)
                    yield result
                except StopIteration:
                    _ = self.iterables.pop(0)
        elif self.restarable:
            yield from self.results

    @classmethod
    def clone(cls, data=None, restarable=True):
        return cls(data, restarable=restarable)

    def concat(self, *iterables):
        self.iterables.extend(iter(i) for i in iterables)
        return self

    def drop_while(self, func):
        self.restarable = True
        return self.clone(itertools.dropwhile(func, self))

    def take_while(self, func):
        return self.clone(itertools.takewhile(func, self))

    def filter(self, func=None):
        self.restarable = True
        return self.clone(
            i for i in self if func is None and i or func(i)
        )

    def map(self, func):
        self.restarable = True
        return self.clone(func(i) for i in self)

    def some(self, func):
        return any(func(i) for i in self)

    def every(self, func):
        return all(func(i) for i in self)
