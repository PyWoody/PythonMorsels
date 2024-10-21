import io
import sys

from contextlib import contextmanager


class WriteSpy:

    def __init__(self, *streams, close=True):
        self.streams = streams
        self.closed = False
        self.close_streams = close

    def __enter__(self):
        return self

    def __exit__(self, *args, **kwargs):
        self.close()

    def write(self, line):
        if self.closed:
            raise ValueError('I/O operation on closed file.')
        for stream in self.streams:
            _ = stream.write(line)
            _ = stream.flush()

    def close(self):
        self.closed = True
        if self.close_streams:
            for stream in self.streams:
                stream.close()

    def writable(self):
        if self.closed:
            raise ValueError('I/O operation on closed file.')
        return all(stream.writable() for stream in self.streams)

    def getvalue(self):
        try:
            return self.streams[0].getvalue()
        except Exception:
            return ''

    @property
    def stdin(self):
        return ''.join(str(i) for i in sys.stdin.readlines())

    @property
    def stderr(self):
        return sys.stderr
        # return ''.join(str(i) for i in sys.stderr.readlines())

    @property
    def stdout(self):
        return ''.join(str(i) for i in sys.stdout.readlines())


@contextmanager
def stdout_spy():
    with WriteSpy(sys.stdout, sys.stderr, close=False) as spy:
        yield spy


@contextmanager
def stdin_spy():
    with WriteSpy(sys.stdin, close=False) as spy:
        yield spy


@contextmanager
def iospy():
    with WriteSpy(sys.stdin, sys.stdout, sys.stderr, close=False) as spy:
        yield spy
