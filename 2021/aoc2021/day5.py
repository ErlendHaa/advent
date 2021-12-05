import re

from collections import Counter

def parse(inputfile):
    return [
        [int(y) for y in re.split(',| -> ', x.strip('\n'))]
        for x
        in open(inputfile).readlines()
    ]

def diagonal(line):
    if line[0] == line[2]: return False
    if line[1] == line[3]: return False
    return True

def overlapping(coordinates):
    return len([c for c in Counter(coordinates).values() if c >= 2])

def coordinates(line, skipdiag):
    isdiag = diagonal(line)
    if isdiag and skipdiag: return

    x1, x2 = line[0], line[2]
    y1, y2 = line[1], line[3]

    if isdiag:
        dx = 1 if x1 < x2 else -1
        dy = 1 if y1 < y2 else -1


        while True:
            yield x1, y1
            if x1 == x2 and y1 == y2: break
            x1 += dx
            y1 += dy

    else:
        for x in range(min(x1, x2), max(x1, x2) + 1):
            for y in range(min(y1, y2), max(y1, y2) + 1):
                yield x, y

def day5_part1(inputfile):
    lines = parse(inputfile)

    coords = []
    for line in lines:
        for coord in coordinates(line, skipdiag = True):
            coords.append(coord)

    return overlapping(coords)

def day5_part2(inputfile):
    lines = parse(inputfile)

    coords = []
    for line in lines:
        for coord in coordinates(line, skipdiag = False):
            coords.append(coord)

    return overlapping(coords)
