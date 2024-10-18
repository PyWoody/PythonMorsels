from collections import Counter
from datetime import datetime, timedelta


def reconcile_accounts(file1, file2):
    file1.sort(key=date_sort)
    file2.sort(key=date_sort)
    file1_counter = Counter()
    file2_counter = Counter()
    for line in file1:
        file1_counter[''.join(line)] += 1
    for line in file2:
        file2_counter[''.join(line)] += 1
    out_file_1 = []
    for line in file1:
        if file2_counter[''.join(line)] > 0:
            out_file_1.append(line + ['FOUND'])
            file2_counter[''.join(line)] -= 1
        else:
            prev_date, next_date = delta_days(line[0])
            tmp_line = line[:]
            tmp_line[0] = prev_date
            if file2_counter[''.join(tmp_line)] > 0:
                out_file_1.append(line + ['FOUND'])
                file2_counter[''.join(tmp_line)] -= 1
            else:
                tmp_line[0] = next_date
                if file2_counter[''.join(tmp_line)] > 0:
                    out_file_1.append(line + ['FOUND'])
                    file2_counter[''.join(tmp_line)] -= 1
                else:
                    out_file_1.append(line + ['MISSING'])
    out_file_2 = []
    for line in file2:
        if file1_counter[''.join(line)] > 0:
            out_file_2.append(line + ['FOUND'])
            file1_counter[''.join(line)] -= 1
        else:
            prev_date, next_date = delta_days(line[0])
            tmp_line = line[:]
            tmp_line[0] = prev_date
            if file1_counter[''.join(tmp_line)] > 0:
                out_file_2.append(line + ['FOUND'])
                file1_counter[''.join(tmp_line)] -= 1
            else:
                tmp_line[0] = next_date
                if file1_counter[''.join(tmp_line)] > 0:
                    out_file_2.append(line + ['FOUND'])
                    file1_counter[''.join(tmp_line)] -= 1
                else:
                    out_file_2.append(line + ['MISSING'])
    return out_file_1, out_file_2


def delta_days(strtime):
    delta = timedelta(days=1)
    date = datetime.strptime(strtime, '%Y-%m-%d')
    prev_date = datetime.strftime(date - delta, '%Y-%m-%d')
    next_date = datetime.strftime(date + delta, '%Y-%m-%d')
    return prev_date, next_date


def date_sort(line):
    return datetime.strptime(line[0], '%Y-%m-%d')

