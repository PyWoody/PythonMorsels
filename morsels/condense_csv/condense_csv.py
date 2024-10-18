import csv


def condense_csv(text, id_name=None):
    header = csv.reader(text.splitlines())
    skip_first = False
    if id_name is None:
        fieldnames = [next(header)[0]]
        skip_first = True
    else:
        fieldnames = [id_name]
    while True:
        try:
            if (col := next(header)[1]) not in fieldnames:
                fieldnames.append(col)
        except StopIteration:
            break
    reader = csv.reader(text.splitlines())
    if skip_first:
        _ = next(reader)
    output = [','.join(fieldnames)]
    prev = None
    output_row = dict.fromkeys(fieldnames, ' ')
    while True:
        try:
            row = next(reader)
        except StopIteration:
            if output_row.values():
                output.append(
                    ','.join(
                        '"' + ','.join(i) + '"' if len(i) > 1 else i[0].strip()
                        for i in csv.reader(output_row.values())
                    )
                )
            return '\n'.join(output)
        else:
            key = row[0]
            if prev is None:
                output_row[fieldnames[0]] = key
            elif key != prev:
                output.append(
                    ','.join(
                        '"' + ','.join(i) + '"' if len(i) > 1 else i[0].strip()
                        for i in csv.reader(output_row.values())
                    )
                )
                output_row = dict.fromkeys(fieldnames, ' ')
                output_row[fieldnames[0]] = key
            output_row[row[1]] = row[2]
            prev = key
