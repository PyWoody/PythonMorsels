def format_fixed_width(rows, padding=2, widths=None, alignments=None):
    if not rows:
        return ''
    spacing = {}
    num_cols = len(rows[0])
    if alignments is None:
        alignments = ['L' for _ in range(num_cols)]
    if widths is None:
        widths = [0 for _ in range(num_cols)]
    for row in rows:
        for col in range(num_cols):
            spacing[col] = max(len(row[col]), spacing.get(col, 0))
    output = []
    for row in rows:
        row_output = ''
        for col in range(num_cols):
            if alignments[col] == 'L':
                item = row[col]
            else:
                item = ''
            item += ' ' * (spacing[col] - len(row[col]))
            if (delta := widths[col] - len(item)) > 0:
                item += ' ' * delta
            if alignments[col] == 'L':
                if padding:
                    item += ' ' * padding
            else:
                item += row[col]
            row_output += item
        output.append(row_output.rstrip())
    return '\n'.join(output)
