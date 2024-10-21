import re
import tokenize


def run(files):
    for file in files:
        for line_num, cur, prev in implicit_concatentions(file):
            print(
                f'{file}, line {line_num} between {cur} and {prev}'
            )


def implicit_concatentions(file):
    start = re.compile(r'''^[rbuU]*(?:"|')''')
    end = re.compile(r'''(?:"|')$''')
    with open(file, 'rb') as f:
        tokens = tokenize.tokenize(f.readline)
        prev_line = ''
        prev_token = None
        for token in tokens:
            if token.string.strip():
                if start.search(token.string.strip()) and end.search(prev_line):
                    yield prev_token.end[0], token.string, prev_token.string
                prev_line = token.string.strip()
                prev_token = token


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('files', nargs='+')
    args = parser.parse_args()

    run(args.files)
