import unicodedata


class FuzzyString:

    def __init__(self, string):
        self.string = str(string)

    def __repr__(self):
        return repr(self.string)

    def __str__(self):
        return self.string

    def __eq__(self, other):
        if isinstance(other, FuzzyString):
            other = other.string
        other = unicodedata.normalize('NFC', other.casefold())
        string = unicodedata.normalize('NFC', self.string.casefold())
        return other == string

    def __lt__(self, other):
        if isinstance(other, FuzzyString):
            return self.string > other.string
        return self.string > other

    def __le__(self, other):
        if isinstance(other, FuzzyString):
            return self.string >= other.string
        return self.string >= other

    def __gt__(self, other):
        if isinstance(other, FuzzyString):
            return self.string < other.string
        return self.string < other

    def __ge__(self, other):
        if isinstance(other, FuzzyString):
            return self.string <= other.string
        return self.string <= other

    def __contains__(self, other):
        if isinstance(other, FuzzyString):
            other = other.string
        forms = ['NFC', 'NFKC', 'NFD', 'NFKD']
        for form in forms:
            other = unicodedata.normalize(form, other.casefold())
            string = unicodedata.normalize(form, self.string.casefold())
            if other in string:
                return True
        return False

    def __add__(self, other):
        cls = self.__class__
        if isinstance(other, FuzzyString):
            return cls(self.string + other.string)
        return cls(self.string + other)

    def __getattr__(self, name):
        if name.casefold() == self.string.casefold():
            return self.string
        raise AttributeError
