import re
import sys
import warnings

from contextlib import contextmanager
from functools import wraps


class error_on_warnings:

    def __init__(self, message='', category=Warning):
        self.message_re = re.compile(message, re.IGNORECASE)
        self.is_re = '.*' in message if message != '' else True
        self.category = category
        self.orig_warnings = warnings.showwarning

    def __call__(self, func):
        @wraps(func)
        def inner(*args, **kwargs):
            with self:
                return func(*args, **kwargs)
        return inner

    def __enter__(self):
        self.orig_warnings = warnings.showwarning
        warnings.showwarning = self.handle_warning
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        warnings.showwarning = self.orig_warnings

    def handle_warning(
        self, message, category, filename, lineno, file=None, line=None
    ):
        if self.is_re:
            if self.message_re.search(str(message)):
                if category is self.category or issubclass(category, self.category):
                    raise category
        elif self.message_re.pattern == message:
            if category is self.category or issubclass(category, self.category):
                raise category
        self.orig_warnings(message, category, filename, lineno, file, line)


class WarningMessage:

    def __init__(
        self, message, category, filename, lineno, file=None, line=None
    ):
        self.message = message
        self.category = category
        self.filename = filename
        self.lineno = lineno
        self.file = file
        self.line = line

    def __repr__(self):
        cls = self.__class__.__name__
        args = [
            f'message={repr(self.message)}',
            f'category={repr(self.category)}',
            f'filename={repr(self.filename)}',
            f'lineno={repr(self.lineno)}',
        ]
        if self.file is not None:
            args.append(f'file={repr(self.file)}')
        if self.line is not None:
            args.append(f'line={repr(self.line)}')
        return f'{cls}({", ".join(args)})'


@contextmanager
def capture_warnings(message='', category=Warning):
    def _track_warnings(
        _message, _category, _filename, _lineno, _file=None, _line=None
    ):
        handled = False
        if is_re:
            if message_re.search(str(_message)):
                if _category is category or issubclass(_category, category):
                    warning = WarningMessage(
                        _message, _category, _filename, _lineno, _file, _line
                    )
                    caught.append(warning)
                    handled = True
        elif message_re.pattern == _message or message_re.pattern == '':
            if _category is category or issubclass(_category, category):
                warning = WarningMessage(
                    _message, _category, _filename, _lineno, _file, _line
                )
                caught.append(warning)
                handled = True
        if not handled:
            sys.stderr.write(str(_message))

    caught = []
    is_re = '.*' in message if message != '' else True
    message_re = re.compile(message, re.IGNORECASE)
    try:
        orig_warnings = warnings.showwarning
        warnings.showwarning = _track_warnings
        yield caught
    finally:
        warnings.showwarning = orig_warnings
