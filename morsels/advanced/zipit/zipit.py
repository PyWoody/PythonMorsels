import os

from zipfile import ZIP_DEFLATED, ZIP_STORED, ZipFile


def zipit(path, deflate=False, as_main=None):
    compression = ZIP_DEFLATED if deflate else ZIP_STORED
    path = os.path.abspath(path)
    project = find_project_name(path)
    fname = f'{project}.zip'
    zip_output_path = os.path.join(os.path.dirname(path), fname)
    with ZipFile(zip_output_path, mode='w', compression=compression) as z:
        if as_main:
            _ = z.writestr('__main__.py', as_python(as_main))
        for src_path, out_path in find_project_files(project, path):
            if not src_path:
                _ = z.mkdir(out_path)
            else:
                _ = z.write(src_path, out_path)


def find_project_name(path):
    if os.path.isfile(path):
        return os.path.split(os.path.splitext(path)[0])[1]
    while True:
        if '__init__.py' in os.listdir(path):
            path = os.path.join(path, '..')
        else:
            return os.path.split(path)[1]


def find_project_files(project, path):
    if os.path.isfile(path):
        yield path, os.path.join(os.path.split(path)[1])
    for root, dirs, files in os.walk(path):
        relpath = os.path.relpath(root, start=path)
        relpath = relpath if relpath != '.' else ''
        yield '', os.path.join(project, relpath)
        for f in files:
            if os.path.splitext(f)[1].lower() == '.py':
                yield os.path.join(root, f), os.path.join(project, relpath, f)


def as_python(command):
    modules, func = command.split(':')
    return '\n\n'.join([f'import {modules}', f'{func}()'])


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('cwd')
    parser.add_argument('--main', '-m')
    parser.add_argument(
        '-0', default=True, action='store_false', dest='deflate'
    )
    args = parser.parse_args()

    zipit(args.cwd, deflate=args.deflate, as_main=args.main)
