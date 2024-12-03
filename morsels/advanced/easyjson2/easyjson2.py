import json

from collections import UserDict, UserList


class JSONObject(UserDict):

    def __getitem__(self, key):
        if isinstance(key, type(Ellipsis)):
            return JSONListObject(self.data.values(), from_get=True)
        return super().__getitem__(key)

    def __getattr__(self, key):
        if key == 'data':
            return super().__getattribute__(key)
        try:
            item = self.data[key]
            if isinstance(item, (dict)):
                return JSONObject(item)
            elif isinstance(item, list):
                return JSONListObject(item)
            else:
                return item
        except KeyError:
            raise AttributeError

    def __setattr__(self, key, value):
        if key == 'data':
            return super().__setattr__(key, value)
        try:
            self.data[key] = value
        except KeyError:
            raise AttributeError

    def __matmul__(self, key):
        return JSONListObject(query(self.data, key))


class JSONListObject(UserList):

    def __init__(self, data, from_get=False):
        self.data = [
            JSONObject(i) if isinstance(i, dict) else i for i in data
        ]
        self.from_get = from_get

    def __getitem__(self, index):
        if isinstance(index, type(Ellipsis)):
            return JSONListObject(self.data, from_get=True)
        if self.from_get:
            if isinstance(index, slice):
                return self.data[index]
            elif isinstance(index, int):
                return JSONListObject(d[index] for d in self.data)
            return JSONListObject(
                v for d in self.data for k, v in d.items() if k == index
            )
        return super().__getitem__(index)

    def __getattr__(self, key):
        if key == 'data':
            return super().__getattr__(key)
        if self.from_get:
            return JSONListObject(
                v for d in self.data for k, v in d.items() if k == key
            )
        return super().__getattr__(key)

    def __matmul__(self, key):
        return JSONListObject(query(self.data, key))


def query(data, key):
    if isinstance(data, (dict, JSONObject)):
        for k, v in data.items():
            if k == key:
                yield v
            yield from query(v, key)
    elif isinstance(data, list):
        for item in data:
            yield from query(item, key)


def parse(string):
    data = json.loads(string)
    if isinstance(data, list):
        return JSONListObject(data)
    return JSONObject(data)
