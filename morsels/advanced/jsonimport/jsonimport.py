import functools
import importlib
import json
import os
import sys

from importlib.abc import Loader, MetaPathFinder


class JSONFinder(MetaPathFinder):

    def find_spec(self, fullname, path, target=None):
        name = fullname.split('.')[-1]
        if path is None:
            paths = sys.path
        else:
            paths = path
        for _path in paths:
            if os.path.isdir(_path):
                for filename in os.listdir(_path):
                    if filename == f'{name}.json':
                        return importlib.machinery.ModuleSpec(
                            name, JSONLoader(_path)
                        )


class JSONLoader(Loader):

    def __init__(self, path):
        self.path = path

    def create_module(self, spec):
        filepath = os.path.join(self.path, f'{spec.name}.json')
        try:
            return json.load(open(filepath, 'r', encoding='utf8'))
        except Exception:
            raise ImportError

    def exec_module(self, module):
        pass


def import_json(filename, paths=None):
    if paths is None:
        paths = ['.']
    filename = f'{filename}.json'
    paths = [os.path.abspath(path) for path in paths]
    for path in paths:
        for file in os.listdir(path):
            if file == filename:
                filepath = os.path.join(path, file)
                try:
                    return json.load(open(filepath, 'r', encoding='utf8'))
                except Exception:
                    raise ImportError


class patch:
    def __init__(self):
        self.finder = JSONFinder()

    def __call__(self, func):
        @functools.wraps(func)
        def inner(*args, **kwargs):
            with self:
                return func(*args, **kwargs)
        return inner

    def __enter__(self, *args, **kwargs):
        sys.meta_path.append(self.finder)

    def __exit__(self, *args, **kwargs):
        sys.meta_path.remove(self.finder)
