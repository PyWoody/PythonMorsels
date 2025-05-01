import functools
import inspect
import textwrap


def coalesce_args(**c_kwargs):

    c_kwargs = {
        k: v if isinstance(v, tuple) else (v,) for k, v in c_kwargs.items()
    }

    def outer(func):
        sig = inspect.signature(func)
        text = []
        if func.__doc__:
            text.append('\n')
            func.__doc__ = textwrap.dedent(func.__doc__.rstrip())
        else:
            func.__doc__ = ''
        for k, v in c_kwargs.items():
            text.append(
                (
                    f'\nIf {k} is {" or ".join(repr(i) for i in v)}'
                    f', replace by {repr(sig.parameters[k].default)}'
                )
            )
        func.__doc__ += textwrap.dedent(''.join(text))

        @functools.wraps(func)
        def inner(*args, **kwargs):
            if args and not kwargs:
                kwargs = {k: a for a, k in zip(args, c_kwargs.keys())}
                for ck, cv in c_kwargs.items():
                    if ck in kwargs and kwargs[ck] in cv:
                        del kwargs[ck]
                return func(*kwargs.values())
            else:
                for ck, cv in c_kwargs.items():
                    if ck in kwargs and kwargs[ck] in cv:
                        del kwargs[ck]
                return func(*args, **kwargs)
        return inner
    return outer
