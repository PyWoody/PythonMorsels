import collections


from numbers import Number


class SetHasher(collections.abc.Set):

    def __init__(self, iterable):
        self.elements = tuple(iterable)

    def __iter__(self):
        yield from self.elements

    def __len__(self):
        return len(self.elements)

    def __contains__(self, value):
        return value in self.elements

    def __hash__(self):
        return self._hash()


class HashWrapper:

    def __init__(self, iterable):
        self.iterable = iterable

    def __eq__(self, other):
        if isinstance(other, HashWrapper):
            return self.iterable == other.iterable
        return self.iterable == other

    def __hash__(self):
        return mutable_hash(self.iterable)


class UnsafeDict(collections.UserDict):

    def __init__(self, data=None):
        # keys: {0: keya}
        # values: {0: valuea}
        self.last_index = 0
        self.key_indexes = dict()
        self.value_indexes = dict()
        if data:
            if isinstance(data, list):
                for k, v in data:
                    self[k] = v
            else:
                for k, v in data.items():
                    self[k] = v

    def __repr__(self):
        data = ', '.join(
            f'{k!r}: {v!r}' for k, v in zip(
                self.key_indexes.values(), self.value_indexes.values()
            )
        )
        return f'{{{data}}}'

    def __len__(self):
        return len(self.key_indexes)

    def __iter__(self):
        yield from self.key_indexes.values()

    def __contains__(self, key):
        key_hash = mutable_hash(key)
        for key in self.key_indexes.values():
            if key_hash == mutable_hash(key):
                return True
        raise False

    def __delitem__(self, key):
        key_hash = mutable_hash(key)
        for index, key in self.key_indexes.items():
            if key_hash == mutable_hash(key):
                del self.key_indexes[index]
                del self.value_indexes[index]
                return
        raise KeyError

    def __getitem__(self, key):
        key_hash = mutable_hash(key)
        for index, existing_key in self.key_indexes.items():
            if key_hash == mutable_hash(existing_key):
                return self.value_indexes[index]
        raise KeyError

    def __setitem__(self, key, value):
        key_hash = mutable_hash(key)
        for index, existing_key in self.key_indexes.items():
            if key_hash == mutable_hash(existing_key):
                self.value_indexes[index] = value
                return value
        self.key_indexes[self.last_index] = key
        self.value_indexes[self.last_index] = value
        self.last_index += 1
        return value

    def keys(self):
        return list(self.key_indexes.values())

    def values(self):
        return list(self.value_indexes.values())



def mutable_hash(obj):
    if isinstance(obj, collections.abc.Hashable):
        if isinstance(obj, (list, tuple)):
            return sum(hash(mutable_hash(i)) for i in obj)
        return hash(obj)
    elif isinstance(obj, dict):
        total = 0
        for k, v in obj.items():
            if isinstance(k, collections.abc.Hashable) and isinstance(v, collections.abc.Hashable):
                total += hash(SetHasher((k, v)))
            else:
                total += mutable_hash(k)
                total += mutable_hash(v)
        return total
    elif isinstance(obj, set):
        return hash(SetHasher(obj))
    return hash(''.join(str(i) for i in obj))
