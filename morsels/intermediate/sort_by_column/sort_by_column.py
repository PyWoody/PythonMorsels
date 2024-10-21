import csv


def csv_sort(csv_file, cols, with_header=False):
    cols = [
        col.split(':') if ':' in col else (col, 'str') for col in cols
    ]
    with open(csv_file, 'r', encoding='utf8', newline='') as f:
        reader = csv.reader(f)
        if with_header:
            print(
                ','.join(
                    f'"{i}"' if ',' in i else i for i in next(reader)
                )
            )
        for col, sort_type in cols[::-1]:
            sort_type = str if sort_type == 'str' else int
            reader = sorted(reader, key=lambda x: sort_type(x[int(col)]))
        for line in reader:
            print(
                ','.join(
                    f'"{i}"' if ',' in i else i for i in line
                )
            )


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('file')
    parser.add_argument('cols', nargs='+')
    parser.add_argument('--with-header', default=False, action='store_true')
    args = parser.parse_args()

    csv_sort(args.file, args.cols, with_header=args.with_header)
