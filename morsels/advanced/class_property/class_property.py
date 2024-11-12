import functools


class class_property:

    def __init__(self, func):
        self.func = func

    def __get__(self, instance, owner=None):
        return self.func(owner)


class class_only_property:

    def __init__(self, func):
        self.func = func

    def __get__(self, instance, owner=None):
        if instance:
            raise AttributeError
        return self.func(owner)


class class_only_method:

    def __init__(self, func):
        self.func = func

    def __get__(self, instance, owner=None):
        if instance:
            raise AttributeError

        @functools.wraps(self.func)
        def inner(*args, **kwargs):
            return self.func(owner, *args, **kwargs)
        return inner
