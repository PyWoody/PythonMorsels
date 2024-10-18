import json

from collections import UserDict


class parse(UserDict):

    def __init__(self, j_data=None, from_attr=False):
        self.from_attr = from_attr
        if j_data is not None:
            self.data = json.loads(j_data)
        else:
            self.data = {}

    def __eq__(self, other):
        if isinstance(other, type(self)):
            return other.data == self.data
        elif isinstance(other, (list, dict, str, int)):
            return other == self.data
        return NotImplemented

    def __getitem__(self, key):
        if isinstance(self.data, list):
            if self.from_attr and isinstance(key, int):
                return self.new(self.data[key])
            if isinstance(key, (str, int)):
                return self.new([item[key] for item in self.data])
            elif isinstance(key, type(Ellipsis)):
                return self.new(self.data)
            else:
                raise KeyError
        if isinstance(key, tuple):
            return self.new({k: self.data[k] for k in key})
        item = self.data[key]
        if isinstance(item, (list, dict)):
            return self.new(item)
        return item

    def __getattr__(self, key):
        if isinstance(self.data, list):
            return self.new([item[key] for item in self.data], from_attr=True)
        item = self.data[key]
        if isinstance(item, (list, dict)):
            return self.new(item)
        return item

    @classmethod
    def new(cls, data, **kwargs):
        return cls(json.dumps(data), **kwargs)
