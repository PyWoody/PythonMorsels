from functools import cached_property


class SuperMap:

    def __init__(self, data, indexes):
        self.indexes = {i for i in indexes}
        self._data = data
        self.mapping = None

    def __repr__(self):
        cls = self.__class__.__name__
        return f'{cls}({", ".join(repr(i) for i in self.data)})'

    def __iter__(self):
        yield from self.data

    def __len__(self):
        return len(self.data)

    def __contains__(self, other):
        if is_hashable(other):
            return other in self.data
        return NotImplemented

    def __eq__(self, other):
        if isinstance(other, type(self)):
            return self.data == other.data
        return self.data == other

    @cached_property
    def data(self):
        return {i for i in self._data}

    def where(self, **queries):
        if any(k not in self.indexes for k in queries):
            raise ValueError
        return type(self)(self._query(**queries), self.indexes)


    def _query(self, **queries):
        if self.mapping is None:
            self.reset()
        sentinel = object()
        output = dict()
        for k, v in queries.items():
            data = self.mapping.get(k, {}).get(v, sentinel)
            if data is not sentinel:
                output.setdefault(k, set()).update(data)
        if values := output.values():
            yield from set.intersection(*values)

    def reset(self):
        self.mapping = {}
        self.update(self.data)

    def add(self, item):
        if self.mapping is None:
            self.reset()
        if hasattr(item, '__dict__'):
            for k, v in item.__dict__().keys():
                self.mapping.setdefault(
                    k, {}
                ).setdefault(
                    v, set()
                ).add(item)
        elif hasattr(item, '__slots__'):
            for slot in item.__slots__:
                self.mapping.setdefault(
                    slot, {}
                ).setdefault(
                    getattr(item, slot), set()
                ).add(item)
        else:
            raise Exception
        self.data.add(item)

    def update(self, items):
        for item in items:
            self.add(item)

    def discard(self, item):
        try:
            self.data.remove(item)
        except KeyError:
            pass
        else:
            self.reset()

    def add_indexes(self, *indexes):
        rebuild = False
        for index in indexes:
            if index not in self.indexes:
                self.indexes.add(index)
                rebuild = True
        if rebuild:
            self.reset()

    def remove_indexes(self, *indexes):
        for index in indexes:
            self.indexes.remove(index)
        self.reset()


def is_hashable(obj):
    return hasattr(obj, '__eq__') and hasattr(obj, '__hash__')
