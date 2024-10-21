import functools
import inspect


def debug_calls(func=None, /, set_break=False):

    def wrapper(func):
        @functools.wraps(func)
        def inner(*args, **kwargs):
            output = f'{func.__name__}('
            if args:
                for a in args:
                    if isinstance(a, str):
                        output += f'{a!r}, '
                    else:
                        output += f'{a}, '
                output = output.rstrip(', ')
            if args and kwargs:
                output += ', '
            if kwargs:
                for k, v in kwargs.items():
                    if isinstance(v, str):
                        output += f'{k}={v!r}, '
                    else:
                        output += f'{k}={v}, '
                output = output.rstrip(', ')
            frame = inspect.currentframe()
            caller = frame.f_back.f_code.co_name
            c_line = frame.f_back.f_lineno
            c_file = frame.f_back.f_code.co_filename
            output += f') called by {caller} in file {c_file!r} on line {c_line}'
            print(output, end='')
            return func(*args, **kwargs)

        return inner
    
    if callable(func):
        # Default
        return wrapper(func)

    return wrapper
