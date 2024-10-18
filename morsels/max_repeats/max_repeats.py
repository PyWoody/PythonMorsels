from collections import Counter


def string_with_most_repeats(strings):
    best_count = 0
    best_string = None
    for string in strings:
        if len(string) > best_count:
            counter = Counter(string)
            if counter.most_common(1)[0][1] > best_count:
                best_count = counter.most_common(1)[0][1]
                best_string = string
    return best_string
