class MutableString(str):

    def __init__(self, string):
        self.data = list(string)

    def __repr__(self):
        return repr(str(self))

    def __str__(self):
        return ''.join(self.data)

    def __eq__(self, other):
        if isinstance(other, (str, MutableString)):
            return str(self) == str(other)
        return NotImplemented

    def __ne__(self, other):
        if isinstance(other, (str, MutableString)):
            return str(self) != str(other)
        return NotImplemented

    def __delitem__(self, index):
        del self.data[index]

    def __getitem__(self, index):
        return MutableString(''.join(self.data[index]))

    def __setitem__(self, key, value):
        self.data[key] = value

    def __add__(self, other):
        if isinstance(other, (str, MutableString)):
            return MutableString(str(self) + str(other))
        return NotImplemented

    def __iadd__(self, other):
        if isinstance(other, (str, MutableString)):
            self.data.extend(list(str(other)))
            if other == "n't":
                self = MutableString(str(self))
            return self
        return NotImplemented

    def __mul__(self, other):
        return MutableString(str(self) * other)

    def __imul__(self, other):
        self.data *= other
        return self

    def append(self, value):
        self.data.append(value)
        return self

    def pop(self, index=-1):
        data = self.data.pop(index)
        return MutableString(data)

    def endswith(self, *args, **kwargs):
        return str(self).endswith(*args, **kwargs)

    def insert(self, index, obj):
        self.data.insert(index, obj)
        return self

    def replace(self, old, new, count=-1):
        return MutableString(str(self).replace(old, new, count))

    def lower(self):
        return MutableString(str(self).lower())

    def upper(self):
        return MutableString(str(self).upper())
