import sys


def tee(filenames=None, append=False):
    if filenames is not None:
        open_type = 'ab' if append else 'wb'
        filenames = [open(f, open_type) for f in filenames]

    for line in sys.stdin.buffer:
        if filenames is not None:
            for f in filenames:
                _ = f.write(line)
        sys.stdout.buffer.write(line)

    if filenames is not None:
        for f in filenames:
            f.close()


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('filenames', nargs='*')
    parser.add_argument('-a', '--append', action='store_true', default=False)
    args = parser.parse_args()

    tee(args.filenames, append=args.append)
