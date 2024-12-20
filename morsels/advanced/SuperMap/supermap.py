class SuperMap:

    def __init__(self, hash_objects, indexes):
        if not all(is_hashable(i) for i in indexes):
            raise TypeError
        self.hash_objects = set(hash_objects)
        self.indexes = list(indexes)
        self.index_map = None

    def __repr__(self):
        cls = self.__class__.__name__
        return f'{cls}({", ".join(repr(i) for i in self)})'

    def __len__(self):
        return len(self.hash_objects)

    def __eq__(self, other):
        if isinstance(other, type(self)):
            if self.hash_objects != other.hash_objects:
                return False
            if self.indexes != other.indexes:
                return False
            return True
        return self.hash_objects == other

    def __iter__(self):
        yield from self.hash_objects

    def __contains__(self, item):
        return item in self.hash_objects

    def add(self, item):
        self.hash_objects.add(item)
        if self.index_map is None:
            self.index_map = build_index_map(self.hash_objects, self.indexes)

    def discard(self, item):
        try:
            self.hash_objects.remove(item)
        except KeyError:
            pass
        else:
            if self.index_map is not None:
                self.index_map = build_index_map(
                    self.hash_objects, self.indexes
                )

    def update(self, *items):
        self.hash_objects.update(*items)
        if self.index_map is not None:
            self.index_map = build_index_map(self.hash_objects, self.indexes)

    def add_indexes(self, *indexes):
        self.indexes.extend(indexes)
        if self.index_map is not None:
            self.index_map = build_index_map(self.hash_objects, self.indexes)

    def remove_indexes(self, *indexes):
        for index in indexes:
            self.indexes.remove(index)
        if self.index_map is not None:
            self.index_map = build_index_map(self.hash_objects, self.indexes)

    def where(self, **kwargs):
        if any(k not in self.indexes for k in kwargs):
            raise ValueError
        if self.index_map is None:
            self.index_map = build_index_map(self.hash_objects, self.indexes)
        matches = []
        for key, value in kwargs.items():
            if index := self.index_map.get(key):
                if objects := index.get(value):
                    matches.append(objects)
        if len(matches) == 0:
            return SuperMap([], self.indexes)
        return SuperMap(set.intersection(*matches), self.indexes)


def build_index_map(hash_objects, indexes):
    output = {}
    for index in indexes:
        for obj in hash_objects:
            if hasattr(obj, index):
                output.setdefault(
                    index, dict()
                ).setdefault(
                    getattr(obj, index), set()
                ).add(obj)
    return output


def is_hashable(obj):
    return hasattr(obj, '__eq__') and hasattr(obj, '__hash__')
