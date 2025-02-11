class Tree:

    def __init__(self, nodes=None):
        self.nodes = build(nodes if nodes is not None else {})

    def __repr__(self):
        cls = self.__class__.__name__
        return f'{cls}({str(self)})'

    def __str__(self):
        return str(to_str(self))

    def __len__(self):
        return sum(1 for i in self)

    def __eq__(self, other):
        if isinstance(other, type(self)):
            return values(self) == values(other)
        return NotImplemented

    def __iter__(self):
        for k, v in self.nodes.items():
            if v:
                yield k

    def __setitem__(self, key, value):
        self.nodes[key] = value

    def __delitem__(self, key):
        del self.nodes[key]

    def __getitem__(self, key):
        if node := self.nodes.get(key):
            return node
        node = type(self)()
        self.nodes[key] = node
        return node

    def __setattr__(self, key, value):
        if key == 'nodes':
            return super().__setattr__(key, value)
        return self.__setitem__(key, value)

    def __getattr__(self, key):
        if key == 'nodes':
            return super().__getattr__(key)
        return self.__getitem__(key)

    __delattr__ = __delitem__

    def update(self, values):
        for key, value in values.items():
            if isinstance(value, list):
                self.nodes[key] = value
            else:
                if node := self.__getitem__(key):
                    node.update(value)
                else:
                    self.__setitem__(key, type(self)(value))


def to_str(tree, output=None):
    if output is None:
        output = {}
    for key, value in tree.nodes.items():
        if isinstance(value, Tree):
            output[key] = to_str(value)
        else:
            output[key] = value
    return output


def build(nodes, output=None):
    if output is None:
        output = {}
    for key, value in nodes.items():
        if isinstance(value, Tree):
            output[key] = build(value)
        elif isinstance(value, list):
            output[key] = value
        else:
            output[key] = Tree(value)
    return output


def values(tree, output=None):
    if output is None:
        output = {}
    for key, value in tree.nodes.items():
        if value:
            if isinstance(value, Tree):
                output[key] = values(value)
            elif isinstance(value, list):
                output[key] = value
            else:
                output[key] = values(Tree(value))
    return output
