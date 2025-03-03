class Tree:

    def __init__(self, initial_data=None):
        self.data = {}
        if initial_data is not None:
            self.update(initial_data)

    def __repr__(self):
        return str(to_dict(self.data))

    def __str__(self):
        cls = self.__class__.__name__
        return f'{cls}({repr(self)})'

    def __eq__(self, other):
        if isinstance(other, type(self)):
            return prune(self.data) == prune(other.data)
        return NotImplemented

    def __len__(self):
        return sum(
            len(v) if isinstance(v, type(self)) else 1
            for v in self.data.values() if v
        )

    def __iter__(self):
        for k, v in self.data.items():
            if v:
                yield k

    def __delitem__(self, key):
        del self.data[key]

    __delattr__ = __delitem__

    def __getattr__(self, key):
        if key == 'data':
            return super().__getattr__(key)
        try:
            return self.data[key]
        except KeyError:
            tree = type(self)()
            self.data[key] = tree
            return tree

    def __getitem__(self, key):
        try:
            return self.data[key]
        except KeyError:
            tree = type(self)()
            self.data[key] = tree
            return tree

    def __setitem__(self, key, value):
        self.data[key] = value

    def __setattr__(self, key, value):
        if key == 'data':
            super().__setattr__(key, value)
        else:
            self.data[key] = value

    def update(self, data):
        for k, v in data.items():
            if k in self.data:
                self.data[k].update(v)
            else:
                self.data[k] = type(self)(v) if isinstance(v, dict) else v

    def prune(self):
        self.data = prune(self.data)


def to_dict(data, output=None):
    if output is None:
        output = {}
    for k, v in data.items():
        if isinstance(v, Tree):
            output[k] = to_dict(v.data)
        else:
            output[k] = v
    return output


def prune(data, output=None):
    if output is None:
        output = {}
    for k, v in data.items():
        if isinstance(v, Tree):
            if result := prune(v.data):
                output[k] = result
        elif v != {}:
            output[k] = v
    return output
