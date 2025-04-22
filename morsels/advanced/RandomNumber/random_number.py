import random


class RandomNumber:

    def __init__(
        self, start=None, stop=None, step=None, cache=False, overwritable=False
    ):
        if start is None and stop is None:
            raise TypeError
        step = int(step) if step is not None else 1
        if stop is None:
            stop = int(start)
            start = 0
        else:
            start = int(start)
            stop = int(stop)
        self.range = (start, stop, step)
        self.cache = bool(cache)
        self.overwritable = bool(overwritable)
        self.storage_name = None

    def __set_name__(self, owner, name):
        self.storage_name = name

    def __set__(self, instance, value):
        if not self.overwritable:
            raise AttributeError
        instance.__dict__[self.storage_name] = value

    def __delete__(self, instance):
        if self.cache or self.overwritable:
            del instance.__dict__[self.storage_name]

    def __get__(self, instance, owner):
        if instance is None:
            return self
        if result := instance.__dict__.get(self.storage_name):
            return result
        obj = owner.__dict__[self.storage_name]
        result = random.randrange(*obj.range)
        if obj.cache:
            instance.__dict__[self.storage_name] = result
        return result
