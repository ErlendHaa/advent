from itertools import combinations
from collections import defaultdict
from collections import deque
from math import atan2
from math import pi

class astroide:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.space = defaultdict(deque)
        self.distance = None

    def __lt__(self, rhs):
        return self.distance < rhs.distance

    def __repr__(self):
        return 'astroide({},{})'.format(self.x, self.y)

    def __hash__(self):
        return hash('{}{}'.format(self.x, self.y))

def parse(path):
    astroides = set()
    with open(path, 'r') as f:
        lines = f.readlines()
        for x, line in enumerate(lines):
            for y, char in enumerate(line):
                if char == '#': astroides.add(astroide(x,y))

    return astroides

def angles(astroides):
    for ast1, ast2 in combinations(astroides, 2):
        theta1 = atan2(ast2.y - ast1.y, ast2.x - ast1.x) + pi
        theta2 = atan2(ast1.y - ast2.y, ast1.x - ast2.x) + pi
        ast1.space[wraprad(theta1)].append(ast2)
        ast2.space[wraprad(theta2)].append(ast1)

def wraprad(rad, shift=-1*pi/2, start=0, end=2*pi):
    rad += shift
    if rad > end:   rad -= 2*pi
    if rad < start: rad += 2*pi
    return rad

if __name__ == '__main__':
    astroides = parse('input.txt')
    angles(astroides)
    station =  max(astroides, key=lambda x: len(x.space))

    # A bit cheaty, but with 263 angles, the 200th astroide is destroyd before
    # turning a full round
    angle = sorted(list(station.space.keys()))[199]
    ast   = min(
        station.space[angle],
        key=lambda a: abs(a.x - station.x) + abs(a.y - station.y)
    )

    part2 = ast.x * 100 + ast.y

    print('Part 1: {}'.format(len(station.space)))
    print('Part 2: {}'.format(part2))
