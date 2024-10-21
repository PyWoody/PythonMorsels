import builtins
import io
import sys
import time


BUILTIN_PRINT = builtins.print
ORIG_STDOUT = sys.stdout
ORIG_STDERR = sys.stderr


class DramaticWrapper(io.TextIOWrapper):

    def __init__(self,*args, **kwargs):
        super().__init__(*args, **kwargs)
        self.char_count = 0

    def write(self, value):
        for char in value:
            self.buffer.write(char)
            self.buffer.flush()
            time.sleep(.2)
            self.char_count += 1

    def __del__(self):
        self.buffer.write(str(self.char_count))
        self.buffer.flush()


def print(*args, sep=' ', end='\n', file=None, flush=True):
    no_sleep = False if file is None else True
    output = sys.stdout if file is None else file
    sep = str(sep) if sep is not None else None
    end = str(end) if end is not None else None
    for arg in args[:-1]:
        for char in str(arg):
            output.write(char)
            if flush:
                output.flush()
            if not no_sleep:
                time.sleep(.2)
        if sep is not None:
            for char in sep:
                output.write(char)
                if flush:
                    output.flush()
                if not no_sleep:
                    time.sleep(.2)
    for char in str(args[-1]):
        output.write(char)
        if flush:
            output.flush()
        if not no_sleep:
            time.sleep(.2)
    if end is not None:
        for char in end:
            output.write(char)
            if flush:
                output.flush()
            if not no_sleep:
                time.sleep(.2)


def start():
    sys.stdout = DramaticWrapper(sys.stdout)
    sys.stderr = DramaticWrapper(sys.stderr)


def stop():
    builtins.print = BUILTIN_PRINT
    sys.stdout = ORIG_STDOUT
    sys.stderr = ORIG_STDERR
