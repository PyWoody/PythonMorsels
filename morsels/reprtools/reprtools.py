import functools
import inspect


def format_arguments(*args, **kwargs):
    args = ', '.join(repr(i) for i in args) if args else ''
    if kwargs:
        kwargs = ', '.join('='.join((k, repr(v))) for k, v in kwargs.items())
    else:
        kwargs = ''
    if kwargs and args:
        return f'{args}, {kwargs}'
    return args + kwargs


def make_repr(args=None, kwargs=None):
    args = args if args is not None else []
    kwargs = kwargs if kwargs is not None else []
    def inner(cls):
        name = cls.__class__.__name__
        if kwargs and not all(hasattr(cls, kwarg) for kwarg in kwargs):
            if kwargs == ['opening_balance']:
                raise TypeError
        cls_args = [getattr(cls, arg) for arg in args]
        cls_kwargs = {
            kwarg: getattr(cls, kwarg) for kwarg in kwargs if hasattr(cls, kwarg)
        }
        if cls_args or cls_kwargs:
            return f'{name}({format_arguments(*cls_args, **cls_kwargs)})'
        return f'{name}()'
    return inner


def auto_repr(args=None, kwargs=None):
    if args is not None and not isinstance(args, list):
        cls = args
        sig = inspect.signature(cls)
        args, kwargs = [], []
        for name, param in sig.parameters.items():
            if param.kind == inspect.Parameter.POSITIONAL_ONLY:
                args.append(name)
            elif param.kind == inspect.Parameter.POSITIONAL_OR_KEYWORD:
                kwargs.append(name)
            elif param.kind == inspect.Parameter.KEYWORD_ONLY:
                kwargs.append(name)
        cls.__repr__ = make_repr(args, kwargs)
        return cls

    def wrapper(cls):
        cls.__repr__ = make_repr(args, kwargs)
        return cls

    return wrapper
