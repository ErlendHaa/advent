from itertools import combinations

def parse(path):
    with open(path) as f:
        return list(map(int, f.readlines()))


def valid(port, i, preamble):
    return any([x for x in combinations(port[i-preamble:i], 2) if sum(x) == port[i]])

def first_violation(port, preamble):
    for i, x in enumerate(port[preamble:], start=preamble):
        if not valid(port, i, preamble): return x

    raise IndexError('No violation')

def find_contiguous_set(port, target):
    imin, imax = 0, 1

    while True:
        seq = sum(port[imin:imax])
        if seq == target:
            return min(port[imin:imax]) + max(port[imin:imax])
        elif seq < target:
            imax += 1

        elif seq > target:
            imin += 1
            imax = imin + 1

def puzzle9(path='inputs/day09.txt'):
    port = parse(path)

    part1 = first_violation(port, 25)
    part2 = find_contiguous_set(port, part1)

    return part1, part2
