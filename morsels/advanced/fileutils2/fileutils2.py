import hashlib
import os

from collections import Counter


def find_duplicates(files):
    if len(files) == 1:
        return []
    output = dict()
    counts = Counter()
    for file in files:
        counts[os.stat(file).st_size] += 1
    for file in files:
        if counts[os.stat(file).st_size] > 1:
            output.setdefault(generate_hash(file), set()).add(file)
    return [matches for matches in output.values() if len(matches) > 1]


def generate_hash(file):
    f_hash = hashlib.md5()
    with open(file, 'rb') as f:
        while chunk := f.read(8192):
            f_hash.update(chunk)
    return f_hash.digest()
