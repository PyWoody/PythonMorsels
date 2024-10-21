import json
import os


def to_jsonl(in_file, out_file=None):
    if out_file is None:
        out_file = f'{os.path.splitext(in_file)[0]}.jsonl'
    j_data = json.load(open(in_file, 'r', encoding='utf8'))
    with open(out_file, 'w', encoding='utf8') as f:
        for item in j_data:
            _ = f.write(json.dumps(dict(item)) + '\n')


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('in_file')
    parser.add_argument('out_file', nargs='?', default=None)
    args = parser.parse_args()

    to_jsonl(args.in_file, args.out_file)
