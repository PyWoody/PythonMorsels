from collections.abc import MutableMapping
from typing import Mapping, Sequence


class Grouper(MutableMapping):

    def __init__(self, iterable=None, *, key=None):
        self.key = key
        mapping = {}
        if iterable is not None:
            if isinstance(iterable, Mapping):
                for v in iterable.values():
                    mapping.setdefault(key(v), []).append(v)
            elif isinstance(iterable, Sequence):
                for i in iterable:
                    mapping.setdefault(key(i), []).append(i)
        self.update(mapping)
        breakpoint()

    def __repr__(self):
        return {k: v for k, v in super().__dict__.items() if k != 'key'}

    def __iter__(self):
        yield from self.__dict__

    def __len__(self):
        return len(self.__dict__)

    def __getitem__(self, key):
        if key == 'key':
            return self.key
        if value := self.__dict__[self.key(key)]:
            return value[0]
        raise KeyError

    def __in__(self, key):
        return key in self.__dict__.keys()

    def __delitem__(self, key):
        del self.__dict__[key]

    def __setitem__(self, key, value):
        self.__dict__[key] = value
