import os

from zipfile import ZipFile, ZIP_DEFLATED, ZIP_STORED


def zipit(path, deflate=False, as_main=None):
    compression = ZIP_DEFLATED if deflate else ZIP_STORED
    path = os.path.abspath(path)
    project = find_project_name(path)
    archive_name = os.path.join(os.path.dirname(path), f'{project}.zip')
    with ZipFile(archive_name, mode='w', compression=compression) as z:
        if as_main:
            _ = z.writestr('__main__.py', as_python(as_main))
        if os.path.isfile(path):
            _ = z.write(path, os.path.split(path)[1])
        else:
            _ = z.mkdir(project)
            for root, dirs, files in os.walk(path):
                relpath = os.path.relpath(root, start=path)
                relpath = relpath if relpath != '.' else ''
                for d in dirs:
                    _ = z.mkdir(os.path.join(project, relpath, d))
                for f in files:
                    if os.path.splitext(f)[1].lower() == '.py':
                        _ = z.write(
                            os.path.join(root, f),
                            os.path.join(project, relpath, f)
                        )


def find_project_name(path):
    if os.path.isfile(path):
        return os.path.split(os.path.splitext(path)[0])[1]
    while '__init__.py' in os.listdir(path):
        path = os.path.join(path, '..')
    return os.path.split(path)[1]


def as_python(command):
    modules, func = command.split(':')
    return f'import {modules}\n\n{func}()'


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('cwd')
    parser.add_argument('-m', '--main')
    parser.add_argument(
        '-0', default=True, action='store_false', dest='deflate'
    )
    args = parser.parse_args()

    zipit(args.cwd, deflate=args.deflate, as_main=args.main)
