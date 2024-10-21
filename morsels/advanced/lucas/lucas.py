import shutil
import textwrap

from functools import lru_cache


@lru_cache
def lucas(n):
    if n == 0:
        return 2
    if n == 1:
        return 1
    return lucas(n-1) + lucas(n-2)


def get(n):
    for i in range(n):
        print(lucas(i))


def fill():
    cols, rows = shutil.get_terminal_size()
    rows -= 1
    max_chars = rows * cols
    output = ''
    n = lucas_numbers()
    while len(output) < max_chars:
        output += f'{next(n)} '
    wrap = textwrap.TextWrapper(width=cols, max_lines=rows, placeholder='')
    print(wrap.fill(output))


class lucas_numbers:

    def __init__(self):
        self.current = 0

    def __iter__(self):
        n = self.__class__()
        while True:
            yield next(n)

    def __next__(self):
        number = lucas(self.current)
        self.current += 1
        return number


if __name__ == '__main__':
    import argparse


    parser = argparse.ArgumentParser()
    parser.add_argument('n', type=int, nargs='?')
    parser.add_argument('--fill', default=False, action='store_true')
    args = parser.parse_args()

    if args.fill:
        fill()
    else:
        if args.n:
            num_lucas = args.n
        else:
            num_lucas = shutil.get_terminal_size().lines - 1
            num_lucas = num_lucas if num_lucas > 0 else 1
        get(num_lucas)
