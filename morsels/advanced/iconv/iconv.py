import sys


def run(*, file=None, from_code=None, to_code=None, output=None, strict=True):
    errors = 'strict' if strict else 'ignore'
    from_code = from_code if from_code is not None else sys.getdefaultencoding()
    to_code = to_code if to_code is not None else sys.getdefaultencoding()
    if not file or file == '-':
        sys.stdin.reconfigure(encoding=from_code, errors=errors)
        in_f = sys.stdin
    else:
        in_f = open(file, 'r', encoding=from_code, errors=errors)
    if output is None:
        sys.stdout.reconfigure(encoding=to_code, errors=errors)
        out_f = sys.stdout
        flush = True
    else:
        out_f = open(output, 'w', encoding=to_code, errors=errors)
        flush = False
    for line in in_f:
        _ = out_f.write(line)
    if flush:
        sys.stdout.flush()
    in_f.close()
    out_f.close()



if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('file', nargs='?')
    parser.add_argument('-f', '--from-code')
    parser.add_argument('-t', '--to-code')
    parser.add_argument('-o', '--output')
    parser.add_argument('-c', default=True, action='store_false')
    args = parser.parse_args()

    run(
        file=args.file,
        from_code=args.from_code,
        to_code=args.to_code,
        output=args.output,
        strict=args.c,
    )
