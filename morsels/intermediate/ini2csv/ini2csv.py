import csv
import re


def ini2csv(ini_file, csv_file):
    lang_type = None
    lang_re = re.compile(r'^\[(\*\.\w+)\]$')
    settings_re = re.compile(r'^(\w+)\s*=\s*(.*)$')
    with open(ini_file, 'r', encoding='utf8') as f:
        with open(csv_file, 'w', newline='') as w:
            writer = csv.writer(w)
            for line in f:
                line = line.strip()
                if match := lang_re.search(line):
                    lang_type = match.group(1)
                elif matches := settings_re.search(line):
                    writer.writerow(
                        [lang_type] + [i for i in matches.groups()]
                    )


def collapsed_ini2csv(ini_file, csv_file):
    lang_re = re.compile(r'^\[(\*\.\w+)\]$')
    settings_re = re.compile(r'^(\w+)\s*=\s*(.*)$')
    output = dict()
    with open(ini_file, 'r', encoding='utf8') as f:
        for line in f:
            line = line.strip()
            if match := lang_re.search(line):
                lang_type = match.group(1)
            elif matches := settings_re.search(line):
                setting, value = matches.groups()
                output.setdefault(lang_type, dict())[setting] = value
    with open(csv_file, 'w', newline='') as f:
        fieldnames = list(output[lang_type].keys())
        writer = csv.DictWriter(f, fieldnames=['header'] + fieldnames)
        writer.writeheader()
        for lang in output:
            row = output[lang]
            row['header'] = lang
            writer.writerow(row)


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('ini_file')
    parser.add_argument('csv_file')
    parser.add_argument('--collapsed', action='store_true', default=False)
    args = parser.parse_args()
    if args.collapsed:
        collapsed_ini2csv(args.ini_file, args.csv_file)
    else:
        ini2csv(args.ini_file, args.csv_file)
