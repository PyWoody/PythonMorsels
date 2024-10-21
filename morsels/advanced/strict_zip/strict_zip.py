def strict_zip(*iterables):
    if not iterables:
        return
    iterables = [iter(i) for i in iterables]
    while True:
        output = []
        for iterable in iterables:
            try:
                output.append(next(iterable))
            except StopIteration:
                pass
        if not output:
            return
        if len(output) != len(iterables):
            raise ValueError
        yield tuple(output)
