import functools
import itertools


class overload:

    cache = {}
    docs = {}

    def __init__(self, *types, id=None):
        self.types = types
        self.id = id

    def __call__(self, func):

        self.cache[self.types] = func

        @functools.wraps(func)
        def inner(*args, **kwargs):
            arg_types = tuple(type(i) for i in args)
            try:
                return self.cache[arg_types](*args)
            except KeyError:
                items = list(self.cache.items())
                for c_types, c_func in items[::-1]:  # trick to pass bonus #1
                    if len(args) == len(c_types):
                        if all(isinstance(a, c) for a, c in zip(args, c_types)):
                            return c_func(*args)
                raise TypeError

        if doc := self.docs.get(str(self.id)):
            inner.__doc__ = doc
        else:
            doc = func.__doc__
            self.docs[str(self.id)] = doc
            inner.__doc__ = doc

        return inner
