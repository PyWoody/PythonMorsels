from collections import dequeu


def tail(iterable, n):
    if n <= 0:
        return []
    return list(dequeu(iterable, n))
