def parse_ranges(ranges):
    for r in ranges.replace('->', '').replace('exit', '').split(','):
        if '-' in r:
            start, stop = r.split('-')
            yield from range(int(start), int(stop) + 1)
        else:
            yield int(r)
