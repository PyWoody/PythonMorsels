class MutableString(str):

    def __init__(self, string):
        self.string = str(string)

    def __repr__(self):
        return repr(self.string)

    def __str__(self):
        return self.string

    def __eq__(self, other):
        if isinstance(other, MutableString):
            return self.string == other.string
        return self.string == other

    def __ne__(self, other):
        return not self.__eq__(other)

    def __iter__(self):
        cls = self.__class__
        for char in self.string:
            yield cls(char)

    def __setitem__(self, key, value):
        if not isinstance(key, (slice, int)):
            raise TypeError
        string_list = list(self.string)
        string_list[key] = str(value)
        self.string = ''.join(string_list)

    def __delitem__(self, key):
        if not isinstance(key, (slice, int)):
            raise TypeError
        string_list = list(self.string)
        del string_list[key]
        self.string = ''.join(string_list)

    def __getitem__(self, key):
        return self.__class__(self.string[key])

    def __add__(self, other):
        return self.__class__(self.string + str(other))

    def __iadd__(self, other):
        self.string += str(other)

    def __len__(self):
        return len(self.string)

    def append(self, value):
        self.string += str(value)

    def replace(self, old, new):
        return self.__class__(super().replace(old, new))

    def lower(self):
        return self.__class__(super().lower())

    def insert(self, index, value):
        string_list = list(self.string)
        string_list.insert(index, value)
        self.string = ''.join(string_list)

    def pop(self, index=-1):
        string_list = list(self.string)
        item = string_list.pop(index)
        self.string = ''.join(string_list)
        return self.__class__(item)
