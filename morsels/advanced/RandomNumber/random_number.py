import random


class RandomNumber:

    def __init__(
        self, start, stop=None, step=None, cache=False, overwritable=False
    ):
        if start is None and stop is None:
            raise TypeError
        self.cache = bool(cache)
        self.overwritable = bool(overwritable)
        self.step = int(step) if step is not None else 1
        if stop is None:
            stop = start
            start = 0
        self.start = int(start)
        self.stop = int(stop)
        self.storage_name = None

    def __set_name__(self, owner, name):
        self.storage_name = name

    def __set__(self, instance, value):
        if not self.overwritable:
            raise AttributeError
        instance.__dict__[self.storage_name] = value

    def __get__(self, instance, owner):
        value = instance.__dict__.get(self.storage_name)
        if value is not None:
            return value
        value = random.randrange(self.start, self.stop, self.step)
        if self.cache:
            instance.__dict__[self.storage_name] = value
        return value

    def __delete__(self, instance):
        if self.overwritable or self.cache:
            del instance.__dict__[self.storage_name]
