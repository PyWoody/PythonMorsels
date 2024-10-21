import itertools


def window(numbers, n, *, fillvalue=None):
    if n <= 0:
        return []
    numbers = iter(numbers)
    output = tuple(itertools.islice(numbers, 0, n))
    if (delta := n - len(output)) > 0:
        output = tuple(list(output) + [fillvalue] * delta)
    yield output
    while next_num := next(numbers, None):
        _, *items = output
        output = tuple(items + [next_num])
        yield output


numbers = [1, 2, 3, 4, 5, 6]
# print(list(window(numbers, 2)))
# [(1, 2), (2, 3), (3, 4), (4, 5), (5, 6)]
print(list(window(numbers, 3)))
# [(1, 2, 3), (2, 3, 4), (3, 4, 5), (4, 5, 6)]
squares = (n**2 for n in numbers)
print(list(window(squares, 4)))
# [(1, 4, 9, 16), (4, 9, 16, 25), (9, 16, 25, 36)]
