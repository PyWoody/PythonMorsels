def duplicates_only(iterable):
    dupes = set()
    added = set()
    output = []
    for i, v in enumerate(iterable):
        if v not in dupes:
            output.append((v, i))
            dupes.add(v)
        elif v in dupes and v not in added:
            added.add(v)
    output = sorted((i for i in output if i[0] in added), key=lambda x: x[1])
    return [i[0] for i in output]
