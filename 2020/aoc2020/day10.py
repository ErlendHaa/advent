import math

def parse(path):
    with open(path) as f:
        return list(map(int, f.readlines()))

def pairwise(iterable):
    it = iter(iterable)
    a = next(it, None)

    for b in it:
        yield (a, b)
        a = b

def combinations(jmps):
    consecutive = 0
    combinations = 1

    for x in jmps:
        if x == 1: consecutive += 1
        if x == 3:
            if consecutive == 2: combinations *= 2
            if consecutive == 3: combinations *= 4
            if consecutive == 4: combinations *= 7
            consecutive = 0

    return combinations

def jumps(adaptors):
    jolt1 = 0
    jolt3 = 0

    jmps = []
    for x, y in pairwise(adaptors):
        if   x + 1 == y: jmps.append(1)
        elif x + 3 == y: jmps.append(3)
        else:
            raise ValueError('incorrect chain')

    return jmps

def puzzle10(path='inputs/day10.txt'):
    adaptors = sorted(parse(path))

    adaptors.insert(0, 0) # add socket
    adaptors.append(adaptors[-1] + 3) # add device adaptor

    jmps = jumps(adaptors)
    part1 = len([x for x in jmps if x==1]) * len([x for x in jmps if x==3])
    part2 = combinations(jmps)

    return part1, part2
