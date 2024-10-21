def fix_newlines(in_file, lf=False, crlf=False):
    lf_type = None
    bad_lf_type = None
    if lf:
        lf_type = b'\n'
    elif crlf:
        lf_type = b'\r\n'
    data = []
    with open(in_file, 'rb') as f:
        for line in f:
            if lf_type is None:
                if line.endswith(b'\r\n'):
                    lf_type = b'\r\n'
                    bad_lf_type = b'\n'
                else:
                    lf_type = b'\n'
                    bad_lf_type = b'\r\n'
            if lf:
                line = line.replace(b'\r\n', b'\n')
            elif crlf:
                line = line.replace(b'\r\n', b'\n').replace(b'\n',b'\r\n')
            data.append(line)
        if not data:
            data.append(b'\n')
        elif not data[-1].endswith(lf_type):
            data[-1] += lf_type
    with open(in_file, 'wb') as f:
        for line in data:
            if not lf and not crlf and bad_lf_type:
                if bad_lf_type == b'\r\n':
                    line = line.replace(b'\r\n', b'\n')
                else:
                    line = line.replace(b'\r\n', b'\n').replace(b'\n',b'\r\n')
            _ = f.write(line)


def print_newlines(in_file):
    with open(in_file, 'r') as f:
        for line in f:
            print(line.strip())


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('fname')
    parser.add_argument('--print', action='store_true', default=False)
    group = parser.add_mutually_exclusive_group()
    group.add_argument('--lf', action='store_true', default=False)
    group.add_argument('--crlf', action='store_true', default=False)
    args = parser.parse_args()

    if args.print:
        print_newlines(args.fname)
    else:
        fix_newlines(args.fname, lf=args.lf, crlf=args.crlf)
