import itertools

SENTINEL = object()


def chunked(iterable, n=1, *, fill=SENTINEL):
    if n < 1:
        raise Exception
    iterator = iter(iterable)
    while batch := tuple(itertools.islice(iterator, n)):
        if len(batch) < n and fill is not SENTINEL:
            batch = batch + tuple([fill] * (n - len(batch)))
        yield batch
