import os
import re
import string


def scan(pattern, filename):
    re_pattern = compile_pattern(pattern)
    if match := re_pattern.match(filename):
        return {k: v for k, v in zip(re_pattern.groupindex, match.groups())}


def format(pattern, data):
    re_pattern = compile_pattern(pattern)
    data_keys = set(data.keys())
    pattern_keys = set(re_pattern.groupindex.keys())
    if pattern_keys.difference(data_keys):
        raise Exception
    for group, repl in data.items():
        pattern = pattern.replace(f'%{group}', repl)
    return pattern


def compile_pattern(pattern):
    groups = set()
    replace_re = '[\d\w\s\…\']*?'
    re_chars = {'.', '[', ']', '?'}
    uppers = set(string.ascii_uppercase)
    output = ['^']
    skip_next = False
    for index, char in enumerate(pattern):
        if skip_next:
            skip_next = False
            continue
        if char == '%':
            if index + 1 < len(pattern) and pattern[index + 1] in uppers:
                group = pattern[index + 1]
                if group in groups:
                    char = f'(?P={group})'
                else:
                    char = f'(?P<{pattern[index + 1]}>{replace_re})'
                    groups.add(group)
                skip_next = True
        elif char in re_chars:
            char = rf'\{char}'
        output.append(char)
    output.append('$')
    return re.compile(''.join(output))


def cli(in_pattern, out_pattern):
    for root, dirs, files in os.walk(os.getcwd()):
        for f in files:
            fpath = os.path.relpath(os.path.join(root, f), start=os.getcwd())
            if scanned_data := scan(in_pattern, fpath):
                output = format(out_pattern, scanned_data)
                print(f'Moving "{fpath}" to "{output}"')
            else:
                raise Exception(fpath)


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('in_pattern', type=str)
    parser.add_argument('out_pattern', type=str)
    args = parser.parse_args()

    cli(args.in_pattern, args.out_pattern)
