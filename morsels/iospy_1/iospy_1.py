import sys

from contextlib import contextmanager


class WriteSpy:

    def __init__(self, *streams, close=True):
        self.streams = streams
        self.close_on_exit = close
        self.closed = False

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        if self.close_on_exit:
            self.close()
        self.closed = True

    def write(self, line):
        if self.closed:
            raise ValueError('I/O operation on closed file.')
        for stream in self.streams:
            _ = stream.write(line)

    def close(self):
        if self.close_on_exit:
            for stream in self.streams:
                stream.close()
        self.closed = True

    def writable(self):
        if self.closed:
            raise ValueError('I/O operation on closed file.')
        return all(stream.writable() for stream in self.streams)

    def getvalue(self):
        pos = self.streams[0].tell()
        self.streams[0].seek(0)
        try:
            return ''.join(self.streams[0].readlines())
        except Exception:
            return ''
        finally:
            self.streams[0].seek(pos)


@contextmanager
def stdout_spy():
    with WriteSpy(sys.stdout, sys.stderr, close=False) as spy:
        yield spy
