class OrderedSet:

    def __init__(self, words):
        self.keys = set()
        self.hash = {}
        for i, v in enumerate(words):
            if v not in self.keys:
                self.hash[i] = v
                self.keys.add(v)

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

    def __getitem__(self, key):
        if key in self.hash:
            return self.hash[key]
        return list(self.hash.values())[key]

    def __iter__(self):
        yield from self.hash.values()

    def add(self, word):
        if word not in self.keys:
            self.hash[len(self) + 1] = word
            self.keys.add(word)

    def discard(self, word):
        if word in self.keys:
            words = [i for i in self.hash.values() if i != word]
            self.hash = {i: v for i, v in enumerate(words)}
            self.keys = set(words)
