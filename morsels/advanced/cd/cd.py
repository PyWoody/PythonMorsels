import os

from tempfile import TemporaryDirectory


class cd:

    def __init__(self, path=None):
        self.paths = []
        self.previous = None
        self.tmp_path = None
        if path is None:
            path = TemporaryDirectory(dir=self.previous, delete=False)
            self.tmp_path = path
            self.current = path.name
        else:
            self.current = os.path.abspath(path)

    def __enter__(self):
        self.paths.append(os.getcwd())
        self.previous = os.getcwd()
        os.chdir(self.current)
        return self

    def __exit__(self, *args, **kwargs):
        os.chdir(self.paths.pop())
        if self.tmp_path:
            self.tmp_path.cleanup()

    enter = __enter__
    exit = __exit__
