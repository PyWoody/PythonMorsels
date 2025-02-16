import copy


class fancy:

    def __init__(self, iterable=None):
        self.iterables = []
        if iterable is not None:
            self.iterables.append(iterable)
        self.filter_funcs = []
        self.map_funcs = []
        self.dropwhile_func = None
        self.takewhile_func = None

    def __iter__(self):
        for iterable in self.iterables:
            for item in iterable:
                for func in self.map_funcs:
                    item = func(item)
                if all(func(item) for func in self.filter_funcs):
                    if self.dropwhile_func:
                        if self.dropwhile_func(item):
                            continue
                        self.dropwhile_func = None
                    if self.takewhile_func and not self.takewhile_func(item):
                        return
                    yield item

    def clone(self):
        c = type(self)()
        c.iterables = copy.copy(self.iterables)
        c.filter_funcs = copy.copy(self.filter_funcs)
        c.map_funcs = copy.copy(self.map_funcs)
        c.dropwhile_func = self.dropwhile_func
        c.takewhile_func = self.takewhile_func
        return c

    def concat(self, *iterables):
        obj = self.clone()
        obj.iterables.extend(iterables)
        return obj

    def drop_while(self, func):
        obj = self.clone()
        obj.dropwhile_func = func
        return obj

    def take_while(self, func):
        obj = self.clone()
        obj.takewhile_func = func
        return obj

    def filter(self, func):
        obj = self.clone()
        obj.filter_funcs.append(func)
        return obj

    def map(self, func):
        obj = self.clone()
        obj.map_funcs.append(func)
        return obj

    def every(self, condition):
        return all(condition(i) for i in self)

    def some(self, condition):
        return any(condition(i) for i in self)
