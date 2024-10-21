import itertools

from collections import UserDict


class OrderedDict(UserDict):

    def __init__(self, initialdata=None):
        self.key_list = []
        self.value_list = []
        self.indexes = {}
        super().__init__(initialdata)

    def __delitem__(self, key):
        try:
            index = self.key_list.index(key)
        except ValueError:
            raise KeyError
        _ = self.key_list.pop(index)
        _ = self.value_list.pop(index)
        del self.indexes[key]
        for k, v in self.indexes.items():
            if v > index:
                self.indexes[k] -= 1
        return super().__delitem__(key)

    def __getitem__(self, key):
        if isinstance(key, slice):
            if key.start:
                start = self.key_list.index(key.start)
            else:
                start = 0
            if key.stop:
                stop = self.key_list.index(key.stop)
            else:
                stop = len(self.value_list)
            return self.value_list[start:stop]
        return super().__getitem__(key)

    def __setitem__(self, key, value, not_found=object()):
        if self.data.get(key, not_found) is not_found:
            self.key_list.append(key)
            self.value_list.append(value)
            self.indexes[key] = len(self.key_list) - 1
        else:
            index = self.key_list.index(key)
            self.value_list[index] = value
        return super().__setitem__(key, value)

    def clear(self):
        self.key_list = []
        self.value_list = []
        self.indexes = {}
        self.data = {}

    def index(self, key):
        return self.indexes[key]

    def keys(self):
        return LazyList(self.key_list)

    def values(self):
        return LazyList(self.value_list)


class LazyList:

    def __init__(self, data):
        self.data = data

    def __iter__(self):
        yield from self.data

    def __getitem__(self, index):
        return self.data[index]
