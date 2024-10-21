import gc
import weakref


_NOT_FOUND = object()
_ORIGINAL = object()


class computed_property:

    def __init__(self, *attrs):
        self.attrs = tuple(attrs)
        self.default = tuple([_ORIGINAL for _ in range((len(self.attrs) + 1))])
        self.storage_name = None
        self.instance_cache = weakref.WeakKeyDictionary()
        self.func = None

    def __set_name__(self, owner, name):
        if self.storage_name is None:
            self.storage_name = name
        elif name != self.storage_name:
            raise TypeError

    def __call__(self, func):
        self.func = func
        return self

    def __get__(self, instance, owner):
        if instance is None:
            return self
        try:
            cache = instance.__dict__
        except AttributeError:
            raise TypeError
        try:
            i_cache = self.instance_cache.get(instance)
        except TypeError:
            self.instance_cache = {}
            i_cache = None
        if i_cache is None:
            self.instance_cache[instance] = {self.attrs: self.default}
            i_cache = self.instance_cache[instance]
        *cached_attrs_values, cached_computed_value = i_cache.get(self.attrs)
        if any(
            cached_attrs_values[i] != getattr(instance, v, _NOT_FOUND)
            for i, v in enumerate(self.attrs)
        ):
            cached_computed_value = self.func(instance)
            cur_attrs = tuple(getattr(instance, i, _NOT_FOUND) for i in self.attrs)
            self.instance_cache[instance][self.attrs] = (
                *cur_attrs, cached_computed_value
            )
        return cached_computed_value

    def __set__(self, instance, value):
        raise AttributeError
