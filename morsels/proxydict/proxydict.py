from collections import UserDict


class ProxyDict(UserDict):

    def __init__(self, *dicts):
        self.orig_dicts = list(dicts)
        self.key_to_dict = dict()
        self.data = dict()
        for d in dicts:
            for k, v in d.items():
                self.data[k] = v
                self.key_to_dict[k] = d

    def __repr__(self):
        return repr(self.restore())

    def __str__(self):
        cls = self.__class__.__name__
        return f'{cls}({", ".join(repr(d) for d in self.orig_dicts)})'

    def __eq__(self, other):
        if isinstance(other, ProxyDict):
            return self.restore() == other.restore()
        return self.restore() == other

    def __setitem__(self, name, value):
        raise TypeError("'ProxyDict' object does not support item assignment")

    def __getitem__(self, name):
        if d := self.key_to_dict.get(name):
            return d[name]
        raise KeyError

    def __missing__(self, key):
        for d in self.orig_dicts:
            if value := d.get(key):
                return value
        raise KeyError

    @property
    def maps(self):
        return self.orig_dicts

    def pop(self, index=-1):
        raise Exception('NO POPPING FOR YOU!')

    def restore(self):
        curr_dict = dict()
        for d in self.orig_dicts:
            for k, v in d.items():
                curr_dict[k] = v
        return curr_dict
