class FFactory:

    def __getattribute__(self, name):
        return Operator(name)


class Operator:

    def __init__(self, field):
        self.field = field

    def __gt__(self, other):
        def evaluate(item):
            if not hasattr(item, self.field):
                return False
            return int(getattr(item, self.field)) > int(other)
        return evaluate

    def __lt__(self, other):
        def evaluate(item):
            if not hasattr(item, self.field):
                return False
            return int(getattr(item, self.field)) < int(other)
        return evaluate

    def __ne__(self, other):
        def evaluate(item):
            if not hasattr(item, self.field):
                return False
            return getattr(item, self.field) != other
        return evaluate

    def __eq__(self, other):
        def evaluate(item):
            if not hasattr(item, self.field):
                return False
            return getattr(item, self.field) == other
        return evaluate

    def __contains__(self, other):
        def evaluate(item):
            if not hasattr(item, self.field):
                return False
            return getattr(item, self.field) in other
        return evaluate


F = FFactory()


class QueryList:

    def __init__(self, iterable):
        self.iterable = list(iterable)

    def __iter__(self):
        yield from self.iterable

    def __repr__(self):
        cls = self.__class__.__name__
        return f'{cls}({", ".join(repr(i) for i in self.iterable)})'

    def append(self, item):
        self.iterable.append(item)

    def attrs(self, *attrs):
        if len(attrs) == 1:
            return [
                getattr(i, attrs[0])
                for i in self.iterable if hasattr(i, attrs[0])
            ]
        output = []
        for i in self.iterable:
            if all(hasattr(i, a) for a in attrs):
                output.append(tuple(getattr(i, a) for a in attrs))
        return output

    def filter(self, *fargs, **filters):
        if fargs:
            return QueryList(
                i for i in self.iterable if all(f(i) for f in fargs)
            )
        else:
            eval_filters = {}
            for _filter, default_value in filters.items():
                field, *func = _filter.split('__')
                eval_filters[field] = find(func)(default_value)
            return QueryList(
                i for i in self.iterable
                if all(func(i, field) for field, func in eval_filters.items())
            )


def find(func):
    if not func:
        return eq
    func = func[0].lower().strip()
    if func == 'gt':
        return gt
    elif func == 'lt':
        return lt
    elif func == 'ne':
        return ne
    elif func == 'eq':
        return eq
    elif func == 'in':
        return _in
    elif func == 'contains':
        return contains
    raise Exception


def gt(initial_value):
    def evaluate(item, attr):
        if not hasattr(item, attr):
            return False
        return int(getattr(item, attr)) > int(initial_value)
    return evaluate


def lt(initial_value):
    def evaluate(item, attr):
        if not hasattr(item, attr):
            return False
        return int(getattr(item, attr)) < int(initial_value)
    return evaluate


def ne(initial_value):
    def evaluate(item, attr):
        if not hasattr(item, attr):
            return False
        return getattr(item, attr) != initial_value
    return evaluate


def eq(initial_value):
    def evaluate(item, attr):
        if not hasattr(item, attr):
            return False
        return getattr(item, attr) == initial_value
    return evaluate


def _in(initial_value):
    def evaluate(item, attr):
        if not hasattr(item, attr):
            return False
        return getattr(item, attr) in initial_value
    return evaluate


def contains(initial_value):
    def evaluate(item, attr):
        if not hasattr(item, attr):
            return False
        return str(initial_value) in str(getattr(item, attr))
    return evaluate
