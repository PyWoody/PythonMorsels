import csv
import os
import random
import shutil


def rename(path, start=1, ext='.py'):
    ext = '.' + ext.strip().lower().lstrip('.')
    path = path if path != '.' else ''
    if path and not os.path.isdir(path):
        raise SystemExit('error')
    out_path = f'{os.path.abspath(path)} anonymized'
    if not os.path.isdir(out_path):
        os.makedirs(out_path, exist_ok=True)
    elif any(os.listdir(out_path)):
        raise SystemExit('error')
    print('Anonymizing:')
    files = list(
        sorted(
            os.path.join(path, i) for i in os.listdir(path if path else None)
            if os.path.splitext(i)[1].lower() == ext
        )
    )
    print('\n'.join(files))
    random.shuffle(files)
    key_file = os.path.join(out_path, 'key.csv')
    with open(key_file, 'w', encoding='utf8', newline='') as c:
        writer = csv.writer(c)
        for i, f in enumerate(files, start=start):
            _ = shutil.copy2(f, os.path.join(out_path, f'{i}{ext}'))
            print(f'{i}{ext}')
            _ = writer.writerow([f'{i}{ext}', os.path.split(f)[1]])
    print(f'Saving files in new directory: {out_path}')


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('path')
    parser.add_argument('--start', type=int, default=1)
    parser.add_argument('--extension', type=str, default='.py')
    args = parser.parse_args()

    rename(args.path, start=args.start, ext=args.extension)
