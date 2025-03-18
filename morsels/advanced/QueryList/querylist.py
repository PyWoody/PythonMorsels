import operator

from functools import partial


class QueryList:

    def __init__(self, items=None):
        self.items = list(items) if items is not None else []

    def __iter__(self):
        yield from self.items

    def append(self, item):
        self.items.append(item)
        return self

    def attrs(self, *attrs):
        if len(attrs) == 1:
            return [getattr(i, attrs[0]) for i in self]
        return [tuple(getattr(i, a) for a in attrs) for i in self]

    def filter(self, *F_args, **filters):
        operators = []
        for k, default_value in filters.items():
            attr, *op = k.split('__')
            operator = OPERATORS[op[0]] if op else OPERATORS['eq']
            operators.append((attr, partial(operator, default_value)))
        return type(self)(
            item for item in self
            if all(func(getattr(item, k)) for k, func in operators) and
            all(f(item) for f in F_args)
        )


class FFactory:

    def __init__(self, key=None):
        self.key = key
        self.func = None
        self.all_funcs = []
        self.any_funcs = []

    def __getattr__(self, key):
        return type(self)(key=key)

    def __call__(self, other):
        if self.all_funcs and self.any_funcs:
            if all(func(other) for func in self.all_funcs):
                if self.func(getattr(other, self.key)):
                    return True
                if any(func(other) for func in self.any_funcs):
                    return True
            return False
        elif self.all_funcs:
            if not self.func(getattr(other, self.key)):
                return False
            return all(func(other) for func in self.all_funcs)
        elif self.any_funcs:
            if self.func(getattr(other, self.key)):
                return True
            return any(func(other) for func in self.any_funcs)
        else:
            return self.func(getattr(other, self.key))

    def __or__(self, other):
        self.any_funcs.append(other)
        return self

    def __and__(self, other):
        self.all_funcs.append(other)
        return self

    def __gt__(self, other):
        self.func = partial(OPERATORS['gt'], other)
        return self

    def __lt__(self, other):
        self.func = partial(OPERATORS['lt'], other)
        return self

    def __eq__(self, other):
        self.func = partial(OPERATORS['eq'], other)
        return self

    def __ne__(self, other):
        self.func = partial(OPERATORS['ne'], other)
        return self

    def __le__(self, other):
        self.func = partial(OPERATORS['le'], other)
        return self

    def __ge__(self, other):
        self.func = partial(OPERATORS['ge'], other)
        return self

    def __contains__(self, other):
        self.func = partial(OPERATORS['contains'], other)
        return self

    def __in__(self, other):
        self.func = partial(OPERATORS['eq'], other)
        return self


F = FFactory()


def _in(obj, value):
    return value in obj


def contains(value, obj):
    return value in obj


OPERATORS = {
    'gt': operator.lt,
    'lt': operator.gt,
    'eq': operator.eq,
    'ne': operator.ne,
    'le': operator.ge,
    'ge': operator.le,
    'contains': contains,
    'in': _in,
}
