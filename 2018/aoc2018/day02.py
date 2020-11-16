from collections import Counter
from itertools import combinations

def parse(fpath):
    with open(fpath) as f:
        return [x.strip('\n') for x in f.readlines()]

def checksum(identificators):
    twos, threes = 0, 0
    for ident in identificators:
        counts = Counter(ident).values()
        if 2 in counts: twos   += 1
        if 3 in counts: threes += 1

    return twos * threes

def match(identificators):
    for x, y in combinations(identificators, 2):
        equal = [ch1 for ch1, ch2 in zip(x, y) if ch1 == ch2]
        if len(equal) == len(x) - 1: break

    return ''.join(equal)

def puzzle2(path='inputs/day02.txt'):
    identificators = parse(path)

    part1 = checksum(identificators)
    part2 = match(identificators)
    return part1, part2
