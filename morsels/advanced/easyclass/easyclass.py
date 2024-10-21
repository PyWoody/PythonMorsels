from typing import get_type_hints


MISSING = object()


class field:

    def __init__(
        self,
        default=MISSING,
        default_factory=MISSING,
        init=True,
        repr=True,
        hash=None,
        compare=True,
        metadata=None,
        kw_only=MISSING,
        iter=True
    ):
        if default is not MISSING and default_factory is not MISSING:
            raise ValueError
        self.storage_name = None
        self.default_factory = default_factory
        self.default = default
        self.init = init
        self.repr = repr
        self.hash = hash
        self.compare = compare
        self.metadata = metadata
        self.kw_only = kw_only
        self.iter = iter

    def __set_name__(self, owner, name):
        self.storage_name = name

    def __get__(self, instance, owner):
        try:
            return instance.__dict__[self.storage_name]
        except KeyError:
            if self.default_factory is not MISSING:
                self.default = self.default_factory()
            instance.__dict__[self.storage_name] = self.default
            return self.default

    def __set__(self, instance, value):
        instance.__dict__[self.storage_name] = value


def easyclass(
    cls=None,
    *,
    iter=True,
    init=True,
    repr=True,
    eq=True,
    order=False,
    unsafe_hash=False,
    frozen=True,
    match_args=True,
    kw_only=False,
    slots=False,
    weakref_slot=False,
    index=False,
):

    if not callable(cls):
        def inner(func):
            return easyclass(
                func,
                iter=iter,
                init=init,
                repr=repr,
                eq=eq,
                order=order,
                unsafe_hash=unsafe_hash,
                frozen=frozen,
                match_args=match_args,
                kw_only=kw_only,
                slots=slots,
                weakref_slot=weakref_slot,
                index=index,
            )
        return inner

    attr_names = get_type_hints(cls).keys()

    def _init(self, *args, **kwargs):
        for name, arg_value in zip(attr_names, args):
            self.__dict__[name] = arg_value
        for k, v in kwargs.items():
            self.__dict__[k] = v
        if getattr(self, '__post_init__', False):
            self.__post_init__()

    def _iter(self):
        for item_name in attr_names:
            if isinstance(cls.__dict__.get(item_name), field):
                if cls.__dict__[item_name].iter:
                    yield getattr(self, item_name)
            else:
                yield getattr(self, item_name)

    def _getitem(self, index):
        return list(self)[index]

    def _repr(self):
        name = self.__class__.__name__
        args = []
        for attr in attr_names:
            if isinstance(cls.__dict__.get(attr), field):
                if cls.__dict__[attr].repr:
                    args.append(attr)
            else:
                args.append(attr)
        args = ', '.join(f'{k}={getattr(self, k)!r}' for k in args)
        return f'{name}({args})'

    def _setattr(self, name, value):
        raise AttributeError

    def _lt(self, other):
        if isinstance(other, type(self)):
            return tuple(self) < tuple(other)
        return NotImplemented

    def _eq(self, other):
        if isinstance(other, type(self)):
            return tuple(self.__no_compares()) == tuple(other.__no_compares())
        return NotImplemented

    def _le(self, other):
        if isinstance(other, type(self)):
            return tuple(self.__no_compares()) <= tuple(other.__no_compares())
        return NotImplemented

    def _gt(self, other):
        if isinstance(other, type(self)):
            return tuple(self.__no_compares()) > tuple(other.__no_compares())
        return NotImplemented

    def _ge(self, other):
        if isinstance(other, type(self)):
            return tuple(self.__no_compares()) >= tuple(other.__no_compares())
        return NotImplemented

    def _hash(self):
        items = []
        for item_name in attr_names:
            if isinstance(cls.__dict__.get(item_name), field):
                item = cls.__dict__[item_name]
                if item.hash or (item.hash is None and item.compare):
                    items.append(getattr(self, item_name))
            else:
                items.append(getattr(self, item_name))
        return hash(tuple(items))

    def _filter_compares(self):
        for item_name in attr_names:
            if isinstance(cls.__dict__.get(item_name), field):
                if cls.__dict__[item_name].compare:
                    yield getattr(self, item_name)
            else:
                yield getattr(self, item_name)

    cls.__init__ = _init
    cls.__eq__ = _eq if eq else raise_type_error
    cls.__iter__ = _iter if iter else raise_type_error
    if index:
        cls.__getitem__ = _getitem
    if order:
        if eq is False:
            cls.__lt__ = raise_value_error
            cls.__le__ = raise_value_error
            cls.__gt__ = raise_value_error
            cls.__ge__ = raise_value_error
        else:
            cls.__lt__ = _lt
            cls.__le__ = _le
            cls.__gt__ = _gt
            cls.__ge__ = _ge
    if repr:
        cls.__repr__ = _repr
    if frozen:
        cls.__setattr__ = raise_attribute_error
    if not unsafe_hash and eq and not frozen:
        cls.__hash__ = raise_type_error
    else:
        cls.__hash__ = _hash
    cls.__no_compares = _filter_compares
    return cls


def raise_attribute_error(*args, **kwargs):
    raise AttributeError


def raise_type_error(*args, **kwargs):
    raise TypeError


def raise_value_error(*args, **kwargs):
    raise ValueError
