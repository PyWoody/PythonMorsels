import os
import re
import string
import sys


def scan(pattern, filename):
    re_pattern = compile_pattern(pattern)
    if match := re_pattern.match(filename):
        return {k: v for k, v in zip(re_pattern.groupindex, match.groups())}


def format(pattern, data):
    re_pattern = compile_pattern(pattern)
    data_keys = set(data.keys())
    pattern_keys = set(re_pattern.groupindex.keys())
    if missing_keys := pattern_keys.difference(data_keys):
        key_str = ', '.join(f'%{k}' for k in missing_keys)
        if len(missing_keys) > 1:
            raise Exception(f"Groups {key_str} weren't captured")
        raise Exception(f"Group {key_str} wasn't captured")
    for group, repl in data.items():
        pattern = pattern.replace(f'%{group}', repl)
    return pattern


def compile_pattern(pattern):
    groups = set()
    replace_re = r'[\d\w\s\…\']*?'
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


def pat_check(in_pattern, out_pattern):
    in_pat_keys = set()
    out_pat_keys = set()
    for index, char in enumerate(in_pattern):
        if char == '%' and index + 1 < len(in_pattern):
            pat = in_pattern[index + 1]
            if pat in in_pat_keys:
                sys.stderr.write(
                    f'Warning: Group %{pat} referenced multiple times\n'
                )
            in_pat_keys.add(pat)
    for index, char in enumerate(out_pattern):
        if char == '%' and index + 1 < len(out_pattern):
            pat = out_pattern[index + 1]
            if pat in out_pat_keys:
                sys.stderr.write(
                    f'Warning: Group %{pat} referenced multiple times\n'
                )
            out_pat_keys.add(pat)
    if diff := in_pat_keys.difference(out_pat_keys):
        diff = ', '.join(f'Group %{i}' for i in diff)
        sys.stderr.write(f'Warning: {diff} not referenced in output\n')


def cli(in_pattern, out_pattern, force=False):
    move_output = []
    for root, dirs, files in os.walk(os.getcwd()):
        for f in files:
            fpath = os.path.relpath(os.path.join(root, f), start=os.getcwd())
            if scanned_data := scan(in_pattern, fpath):
                try:
                    output = format(out_pattern, scanned_data)
                except Exception as e:
                    sys.stderr.write(f'{str(e).strip()}\n')
                else:
                    move_output.append((fpath, output))
    if force:
        pat_check(in_pattern, out_pattern)
        for fpath, output in sorted(move_output):
            print(f'Moving "{fpath}" to "{output}"')
            os.makedirs(os.path.dirname(output), exist_ok=True)
            os.rename(fpath, output)
    else:
        for fpath, output in sorted(move_output):
            print(f'Move "{fpath}" to "{output}"?')
        pat_check(in_pattern, out_pattern)
        response = input('Perform all the above actions? [y/N] ')
        if response.strip().lower() == 'y':
            for fpath, output in sorted(move_output):
                print(f'Moving "{fpath}" to "{output}"')
                os.makedirs(os.path.dirname(output), exist_ok=True)
                os.rename(fpath, output)


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('in_pattern', type=str)
    parser.add_argument('out_pattern', type=str)
    parser.add_argument('-f', '--force', action='store_true', default=False)
    args = parser.parse_args()

    cli(args.in_pattern, args.out_pattern, force=args.force)
