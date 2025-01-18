import string


def split(
    filename,
    max_lines=1_000,
    max_chars=0,
    numeric_chars=False,
    number_chars=2
):
    tail_chars = next_letter(
        numeric_chars=numeric_chars, number_chars=number_chars
    )
    if max_chars > 0:
        return split_by_chars(filename, tail_chars, max_chars)
    return split_by_lines(filename, tail_chars, max_lines)


def split_by_chars(filename, tail_chars, max_chars):
    with open(filename, 'r', encoding='utf8') as src:
        output_file = open(
            f'{filename}.{next(tail_chars)}', 'w', encoding='utf8'
        )
        char_count = 0
        for line in src:
            if char_count + len(line) > max_chars:
                char_count = 0
                output_file.close()
                output_file = open(
                    f'{filename}.{next(tail_chars)}', 'w', encoding='utf8'
                )
            _ = output_file.write(line)
            char_count += len(line)
    output_file.close()


def split_by_lines(filename, tail_chars, max_lines):
    with open(filename, 'r', encoding='utf8') as src:
        output_file = open(
            f'{filename}.{next(tail_chars)}', 'w', encoding='utf8'
        )
        for index, line in enumerate(src):
            if index > 0 and index % max_lines == 0:
                output_file.close()
                output_file = open(
                    f'{filename}.{next(tail_chars)}', 'w', encoding='utf8'
                )
            _ = output_file.write(line)
    output_file.close()


def next_letter(numeric_chars=False, number_chars=2):
    if numeric_chars:
        num = 0
        while True:
            yield str(num).zfill(number_chars)
            num += 1
    else:
        letters = list(string.ascii_lowercase)
        if number_chars == 1:
            yield from letters
        for head in letters:
            for tail in letters:
                yield f'{head}{tail}'


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('file')
    parser.add_argument('-l', '--max-lines', default=1_000, type=int)
    parser.add_argument('-C', '--max-chars', default=0, type=int)
    parser.add_argument('-a', '--number-chars', default=2, type=int)
    parser.add_argument(
        '-d', '--numeric-chars', default=False, action='store_true'
    )
    args = parser.parse_args()

    split(
        args.file,
        max_lines=args.max_lines,
        max_chars=args.max_chars,
        numeric_chars=args.numeric_chars,
        number_chars=args.number_chars,
    )
