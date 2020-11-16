from itertools import combinations

import re

def parse(fpath):
    with open(fpath) as f:
        lines = [re.split(' @ |,|: |x',x.strip('\n').strip('#')) for x in f.readlines()]

    claims = {}
    for line in lines:
        line = list(map(int, line))
        claims[line[0]] = line[1:]
    return claims

class point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __repr__(self):
        return 'point(x={}, y={})'.format(self.x, self.y)

    def __hash__(self):
        return hash(self.__repr__())

    def __eq__(self, rhs):
        return ((self.x == rhs.x) and (self.y == rhs.y))

def generate_points(x0, y0, xmax, ymax):
    for x in range(x0, x0 + xmax):
        for y in range(y0, y0 + ymax):
            yield point(x, y)

def puzzle3(path='inputs/day03.txt'):
    claims = parse(path)

    fabric = set()
    collisions = set()
    for _, claim in claims.items():
        for point in generate_points(*claim):
            if point in fabric: collisions.add(point)
            else: fabric.add(point)

    non_overlapping = -1
    for name, claim in claims.items():
        if any([x for x in generate_points(*claim) if x in collisions]):
            continue

        non_overlapping = name
        break

    return len(collisions), non_overlapping
