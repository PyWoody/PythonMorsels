from contextlib import contextmanager
from tempfile import NamedTemporaryFile


@contextmanager
def make_file(
    contents=None, directory=None, encoding=None, mode='w', newline=None
):
    if 'b' in mode:
        file = NamedTemporaryFile(dir=directory, mode=mode)
    else:
        file = NamedTemporaryFile(
            dir=directory, encoding=encoding, mode=mode, newline=newline
        )
    if contents:
        if 'b' in mode:
            if not isinstance(contents, bytes):
                contents = contents.encode(
                    encoding if encoding is not None else 'utf8'
                )
            _ = open(file.name, mode).write(contents)
        else:
            _ = open(
                file.name, mode, encoding=encoding, newline=newline
            ).write(contents)
    try:
        yield file.name
    finally:
        file.close()
