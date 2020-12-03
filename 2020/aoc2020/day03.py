import numpy as np

from .point import Point

def parse(path):
    with open(path) as f:
        return np.array([
            [x for x in line.strip('\n')]
            for line in f.readlines()
        ])

class area_map:
    def __init__(self, area):
        self.area    = area
        self.pos     = Point(0, 0)
        self.xwrap   = 0
        self.xstride = len(self.area[0])
        self.ymax    = len(self.area)

    def position(self):
        return Point(self.pos.x + self.xwrap * self.xstride, self.pos.y)

    def ontree(self):
        if self.area[self.pos.y, self.pos.x] == '#': return True
        else:                                        return False

    def reset(self):
        self.pos   = Point(0,0)
        self.xwrap = 0
        return self

    def move(self, Point):
        pos = self.position()

        ypos = pos.y + Point.y
        if ( ypos >= self.ymax ):
            raise IndexError("Y out of bounds")

        self.pos.y = ypos
        self.pos.x = (pos.x + Point.x)  % self.xstride
        self.xwrap = (pos.x + Point.x) // self.xstride


def traverse(area, step):
    trees = 0
    while True:
        if area.ontree(): trees += 1

        try:               area.move(step)
        except IndexError: break

    return trees

def puzzle3(path='inputs/day03.txt'):
    area = area_map( parse(path) )

    part1 = traverse(area, Point(3, 1))

    slopes = [Point(1, 1), Point(3, 1), Point(5, 1), Point(7, 1), Point(1, 2)]
    part2  = np.prod([traverse(area.reset(), x) for x in slopes])

    return part1, part2
