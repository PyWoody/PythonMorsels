from collections import namedtuple

LoopItem = namedtuple(
    'LoopItem', ['is_first', 'index', 'current', 'previous', 'is_last', 'next']
)

def loop_helper(iterable, previous_default=None, next_default=None):
    if not iterable:
        return
    output = list(iterable)
    if len(output) == 1:
        yield output[0], LoopItem(
            is_first=True,
            index=0,
            current=output[0],
            previous=previous_default,
            next=next_default,
            is_last=True,
        )
        return
    for i, v in enumerate(zip(output, output[1:])):
        cur, nex = v
        if i == 0:
            yield cur, LoopItem(
                is_first=True,
                index=0,
                current=cur,
                previous=previous_default,
                next=nex, is_last=False,
            )
        else:
            yield cur, LoopItem(
                is_first=False,
                index=i,
                current=cur,
                previous=prev,
                next=nex,
                is_last=False,
            )
        prev = cur
    if len(output) > 1:
        yield output[-1], LoopItem(
            is_first=False,
            index=i+1,
            current=output[-1],
            previous=prev,
            next=next_default,
            is_last=True,
        )
