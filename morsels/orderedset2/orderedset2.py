class KeyValueError(KeyError, ValueError):
    pass

class OrderedSet:

    def __init__(self, words=None):
        self.keys = set()
        self.hash = {}
        if words is not None:
            for word in words:
                self.add(word)

    def __repr__(self):
        cls = self.__class__.__name__
        return f'{cls}([{", ".join(repr(i) for i in self.hash.values())}])'

    __str__ = __repr__

    def __hash__(self):
        return hash(tuple(self.hash.items()))

    def __len__(self):
        return len(self.keys)

    def __contains__(self, item):
        return item in self.keys

    def __eq__(self, other):
        if isinstance(other, set):
            return self.keys == other
        elif isinstance(other, OrderedSet):
            return list(self.hash.values()) == list(other.hash.values())
        return False

    def __sub__(self, other):
        if isinstance(other, type(self)):
            return self.from_words(
                [i for i in self.hash.values() if i not in other.keys]
            )
        elif isinstance(other, set):
            return self.from_words(
                [i for i in self.hash.values() if i not in other]
            )
        return NotImplemented

    def __isub__(self, other):
        if isinstance(other, type(self)):
            self.reset([i for i in self.hash.values() if i not in other.keys])
            return self
        elif isinstance(other, set):
            self.reset([i for i in self.hash.values() if i not in other])
            return self
        return NotImplemented

    def __and__(self, other):
        if isinstance(other, type(self)):
            return self.from_words(
                [i for i in self.hash.values() if i in other.keys]
            )
        elif isinstance(other, set):
            return self.from_words(
                [i for i in self.hash.values() if i in other]
            )
        return NotImplemented

    def __iand__(self, other):
        if isinstance(other, type(self)):
            self.reset(
                [i for i in self.hash.values() if i in other.keys]
            )
            return self
        elif isinstance(other, set):
            self.reset(
                [i for i in self.hash.values() if i in other]
            )
            return self
        return NotImplemented

    def __xor__(self, other):
        output = []
        if isinstance(other, type(self)):
            for i in self.hash.values():
                if i not in other.keys:
                    output.append(i)
            for i in other.hash.values():
                if i not in self.keys:
                    output.append(i)
        elif isinstance(other, set):
            for i in self.hash.values():
                if i not in other:
                    output.append(i)
            for i in other:
                if i not in self.keys:
                    output.append(i)
        if output:
            return self.from_words(output)
        return NotImplemented

    def __ixor__(self, other):
        output = []
        if isinstance(other, type(self)):
            for i in self.hash.values():
                if i not in other.keys:
                    output.append(i)
            for i in other.hash.values():
                if i not in self.keys:
                    output.append(i)
        elif isinstance(other, set):
            for i in self.hash.values():
                if i not in other:
                    output.append(i)
            for i in other:
                if i not in self.keys:
                    output.append(i)
        if output:
            self.reset(output)
            return self
        return NotImplemented

    def __or__(self, other):
        output = []
        if isinstance(other, type(self)):
            for i in self.hash.values():
                output.append(i)
            for i in other.hash.values():
                if i not in self.keys:
                    output.append(i)
        elif isinstance(other, set):
            for i in self.hash.values():
                output.append(i)
            for i in other:
                if i not in self.keys:
                    output.append(i)
        if output:
            return self.from_words(output)
        return NotImplemented

    def __ior__(self, other):
        output = []
        if isinstance(other, type(self)):
            for i in self.hash.values():
                output.append(i)
            for i in other.hash.values():
                if i not in self.keys:
                    output.append(i)
        elif isinstance(other, set):
            for i in self.hash.values():
                output.append(i)
            for i in other:
                if i not in self.keys:
                    output.append(i)
        if output:
            self.rset(output)
            return self
        return NotImplemented

    def __delitem__(self, index):
        _ = self.pop(index)

    def __getitem__(self, key):
        if key in self.hash:
            return self.hash[key]
        return list(self.hash.values())[key]

    def __setitem__(self, key, value):
        if key < 0:
            key = self.index(self.__getitem__(key))
        if value in self.keys:
            if self.index(value) != key:
                raise ValueError
            return
        output = {}
        for k, v in self.hash.items():
            if k != key:
                output[k] = v
            else:
                output[k] = value
                self.keys.remove(v)
                self.keys.add(value)
        self.hash = output

    def __iter__(self):
        yield from self.hash.values()

    def __reversed__(self):
        index = len(self)
        while index > 0:
            index -= 1
            yield self.hash[index]

    @classmethod
    def from_words(cls, words):
        return cls(words)

    def add(self, word):
        if word not in self.keys:
            self.hash[len(self)] = word
            self.keys.add(word)

    def append(self, word):
        if word in self.keys:
            raise ValueError(
                f'{repr(word)} in already in {self.__class__.__name__}'
            )
        self.hash[len(self)] = word
        self.keys.add(word)

    def count(self, word):
        return 1 if word in self.keys else 0

    def discard(self, word):
        if word in self.keys:
            words = [i for i in self.hash.values() if i != word]
            self.hash = {i: v for i, v in enumerate(words)}
            self.keys = set(words)

    def index(self, word):
        try:
            return next(k for k, v in self.hash.items() if v == word)
        except StopIteration:
            raise ValueError

    def pop(self, index=-1):
        word = self[index]
        self.remove(word)
        return word

    def remove(self, word):
        if word not in self.keys:
            raise KeyValueError
        words = [i for i in self.hash.values() if i != word]
        self.hash = {i: v for i, v in enumerate(words)}
        self.keys = set(words)

    def reset(self, words=None):
        self.keys = set()
        self.hash = {}
        if words:
            for word in words:
                self.add(word)
