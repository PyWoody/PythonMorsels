_NOT_FOUND = object()


class cached_property:

    def __init__(self, func):
        self.func = func
        self.storage_name = None
        self.delete_func = None
        self.set_func = None

    def __set_name__(self, owner, name):
        if self.storage_name is None:
            self.storage_name = name
        elif name != self.storage_name:
            raise TypeError

    def __get__(self, instance, owner):
        if instance is None:
            return self
        if self.storage_name is None:
            raise TypeError
        try:
            cache = instance.__dict__
        except AttributeError:
            raise TypeError
        value = cache.get(self.storage_name, _NOT_FOUND)
        if value is _NOT_FOUND:
            value = self.func(instance)
            cache[self.storage_name] = value
        return value

    def __set__(self, instance, value):
        if self.set_func:
            self.set_func(instance, value)
        instance.__dict__[self.storage_name] = value

    def __delete__(self, instance):
        if self.delete_func:
            self.delete_func(instance)
        del instance.__dict__[self.storage_name]

    def setter(self, instance):
        self.set_func = instance
        return self

    def deleter(self, instance):
        self.delete_func = instance
        return self

