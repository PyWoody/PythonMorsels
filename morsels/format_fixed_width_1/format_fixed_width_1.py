import itertools


def format_fixed_width(rows, *, widths=None, padding=2, alignments=None):
    if not rows:
        return ''
    if widths is not None:
        widths = itertools.cycle(widths)
        alignments = ['L']
    if alignments is None:
        alignments = ['L']
    alignments = itertools.cycle(alignments)
    col_max_chars = {}
    num_rows = len(rows)
    num_cols = len(rows[0])
    for row in rows:
        for col in range(num_cols):
            col_max_chars[col] = max(col_max_chars.get(col, 0), len(row[col]))
    output = []
    for row in range(num_rows):
        row_output = []
        for col in range(num_cols):
            word = rows[row][col]
            if widths:
                if col < num_cols:
                    ws = next(widths) + padding - len(word)
                else:
                    ws = 0
            else:
                min_chars = col_max_chars[col]  # at least this many chars
                ws = min_chars - len(word) + padding
            row_output.append(align(word, next(alignments), ws, padding))
        row_output[-1] = row_output[-1].rstrip()
        output.append(''.join(row_output))
    return '\n'.join(output)



def align(word, alignment, whitespace, padding=0):
    if alignment == 'L':
        return f'{word}{" " * whitespace}'
    elif alignment == 'R':
        return f'{" " * (whitespace - padding)}{word}'
    raise NotImplementedError



print(format_fixed_width([['green', 'red'], ['blue', 'purple']]))
rows = [['Robyn', 'Henry', 'Lawrence'], ['John', 'Barbara', 'Gross'], ['Jennifer', '', 'Bixler']]
print('DEFAULT')
print(format_fixed_width(rows))
# Robyn     Henry    Lawrence
# John      Barbara  Gross
# Jennifer           Bixler
print('PADDING=1')
print(format_fixed_width(rows, padding=1))
# Robyn    Henry   Lawrence
# John     Barbara Gross
# Jennifer         Bixler
print('PADDING=3')
print(format_fixed_width(rows, padding=3))
print('WIDTHS=[10, 10, 10]')
rows = [["Jane", "", "Austen"], ["Samuel", "Langhorne", "Clemens"]]
print(format_fixed_width(rows, widths=[10, 10, 10]))
# Jane                    Austen
# Samuel      Langhorne   Clemens
print(format_fixed_width([
                ['NN', 'Artist', 'Title', 'Time'],
                ['03', 'Paul Simon', 'Peace Like a River', '3:23'],
                ['16', 'Johnny Cash', 'Personal Jesus', '3:20'],
                ['', '', '', '1:09:32']
            ], alignments=['L', 'L', 'L', 'R']))
# NN  Artist       Title                  Time
# 03  Paul Simon   Peace Like a River     3:23
# 16  Johnny Cash  Personal Jesus         3:20
#                                      1:09:32
