_NOT_FOUND = object()
_ORIGINAL = object()


class computed_property:

    def __init__(self, *attrs):
        self.attrs = tuple(attrs)
        self.storage_name = None
        self.func = None
        self.set_func = None

    def __set_name__(self, owner, name):
        self.storage_name = name

    def __call__(self, func):
        self.func = func
        return self

    def __set__(self, instance, value):
        if self.set_func is None:
            raise AttributeError
        self.set_func(instance, value)
        instance.__dict__['instance_cache'] = {}

    def __get__(self, instance, owner):
        if instance is None:
            return self
        try:
            cache = instance.__dict__
        except AttributeError:
            raise TypeError
        i_cache = cache.get('instance_cache')
        if not i_cache or not i_cache.get(self.attrs):
            cached_computed_value = self.func(instance)
            cur_attrs = tuple(getattr(instance, i, _NOT_FOUND) for i in self.attrs)
            cache.setdefault('instance_cache', {})[self.attrs] = (
                *cur_attrs, cached_computed_value
            )
        else:
            *cached_values, cached_computed_value = cache['instance_cache'].get(self.attrs)
            if any(
                cached_values[i] != getattr(instance, v, _NOT_FOUND)
                for i, v in enumerate(self.attrs)
            ):
                cached_computed_value = self.func(instance)
                cur_attrs = tuple(getattr(instance, i, _NOT_FOUND) for i in self.attrs)
                cache['instance_cache'][self.attrs] = (
                    *cur_attrs, cached_computed_value
                )
        return cached_computed_value

    def setter(self, func):
        self.set_func = func
        return self
