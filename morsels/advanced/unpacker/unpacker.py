from collections import UserDict


class Unpacker(UserDict):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def __repr__(self):
        cls = self.__class__.__name__
        return f'{cls}({", ".join("=".join((k, repr(v))) for k, v in self.data.items())})'

    def __iter__(self):
        yield from self.data.values()

    def __getitem__(self, key):
        if isinstance(key, tuple):
            output = []
            for k in key:
                output.append(super().__getitem__(k))
            return tuple(output)
        return super().__getitem__(key)

    def __getattr__(self, key):
        if key != 'data':
            return super().__getitem__(key)
        return super().__getattr__(key)

    def __setattr__(self, key, value):
        try:
            super().__getitem__(key)
        except (KeyError, AttributeError):
            super().__setattr__(key, value)
        if key != 'data':
            self.data[key] = value

    def __setitem__(self, key, value):
        if isinstance(key, tuple):
            keys = list(key)
            values = list(value)
            if len(keys) != len(values):
                raise ValueError
            for k, v in zip(keys, values):
                self.data[k] = v
        else:
            self.data[key] = value
