def interleave(*iterables):
    iterables = [iter(i) for i in iterables if i]
    while iterables:
        to_remove = []
        for iterable in iterables:
            try:
                yield next(iterable)
            except StopIteration:
                to_remove.append(iterable)
        for iterable in to_remove:
            _ = iterables.remove(iterable)
