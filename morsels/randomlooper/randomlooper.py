import random


class RandomLooper:

    def __init__(self, *colors):
        self.colors = [i for color in colors for i in color]

    def __len__(self):
        return len(self.colors)

    def __iter__(self):
        colors = list(self.colors)
        random.shuffle(colors)
        yield from colors
