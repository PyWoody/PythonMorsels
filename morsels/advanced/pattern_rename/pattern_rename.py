import os
import re


def scan(pattern, string):
    regex = build(pattern)
    if match := regex.match(string):
        return match.groupdict()


def format(pattern, data):
    regex = build(pattern)
    data_keys = set(data.keys())
    pattern_keys = set(regex.groupindex.keys())
    if pattern_keys.difference(data_keys):
        raise Exception
    for group, repl in data.items():
        group = group.replace('digit', '')
        pattern = pattern.replace(f'%{group}', repl)
    return pattern


def build(pattern):
    output = ['^']
    groups = set()
    skip = False
    for index, char in enumerate(pattern, start=1):
        if skip:
            skip = False
            continue
        if char == '%' and len(pattern) > index:
            skip = True
            if pattern[index] in groups:
                output.append(f'(?P={pattern[index]})')
            elif pattern[index].isupper():
                output.append(f'(?P<{pattern[index]}>[^/]*?)')
                groups.add(pattern[index])
            elif pattern[index].islower():
                output.append(f'(?P<{pattern[index]}>[^/\s]*?)')
                groups.add(pattern[index])
            elif pattern[index].isdigit():
                output.append(f'(?P<digit{pattern[index]}>[\d]*?)')
                groups.add(pattern[index])
            else:
                output.append(re.escape(char))
                skip = False
        else:
            output.append(re.escape(char))
    output.append('$')
    return re.compile(r''.join(output))


def cli(in_pattern, out_pattern):
    for root, dirs, files in os.walk(os.getcwd()):
        for f in files:
            fpath = os.path.relpath(os.path.join(root, f), start=os.getcwd())
            if scanned_data := scan(in_pattern, fpath):
                output = format(out_pattern, scanned_data)
                print(f'Moving "{fpath}" to "{output}"')
            else:
                # raise Exception(fpath)
                pass


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('in_pattern', type=str)
    parser.add_argument('out_pattern', type=str)
    args = parser.parse_args()

    cli(args.in_pattern, args.out_pattern)
