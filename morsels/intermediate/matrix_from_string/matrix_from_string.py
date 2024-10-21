def matrix_from_string(string):
    if not string:
        return []
    return [
        [float(i) for i in s.split(' ') if i]
        for s in string.split('\n') if s.strip()
    ]
