import random
import numpy as np

from intcode import computer
from collections import deque

def parse(path):
    with open(path, mode='r') as f:
        return [int(x) for x in f.readline().split(',')]

NORTH, SOUTH, WEST, EAST,= 1, 2, 3, 4

WALL    = 0
MOVED   = 1
UNKNOWN = 1
GOAL    = 2
START   = 3
FREE    = 4

roadrules = {
    NORTH : EAST,
    EAST  : SOUTH,
    SOUTH : WEST,
    WEST  : NORTH
}

def direction(d):
    if d == NORTH: return 'NORTH'
    if d == SOUTH: return 'SOUTH'
    if d == EAST: return 'EAST'
    if d == WEST: return 'WEST'

def stat(s):
    if s == WALL: return 'WALL'
    if s == MOVED: return 'MOVED'
    if s == GOAL: return 'GOAL'

def draw(area):
    out = []
    for x, line in enumerate(area):
        for y, point in enumerate(line):
            if   point == WALL: out.append('#')
            elif point == FREE: out.append(' ')
            elif point == UNKNOWN: out.append('.')
            elif point == GOAL: out.append('x')
            elif point == START: out.append('s')
        out.append('\n')
    out.append('\n')
    print(''.join(out))

def updatemap(area, x, y, facing, status):
    if   status == MOVED: front = FREE
    elif status == WALL:  front = WALL
    elif status == GOAL:  front = GOAL

    if   facing == NORTH: area[x-1, y] = front
    elif facing == SOUTH: area[x+1, y] = front
    elif facing == EAST:  area[x, y+1] = front
    elif facing == WEST:  area[x, y-1] = front

    return area

def explore(area, x, y):
    facing = random.choice(range(1,5))
    if   facing == NORTH: return x - 1, y
    elif facing == SOUTH: return x + 1, y
    elif facing == WEST: return x, y - 1
    elif facing == EAST: return x, y + 1

def maparea(com):
    facing = NORTH

    x, y = 25, 50
    area = np.reshape(np.ones(50*100), (50, 100))
    area[x, y] = START

    while True:
        com.update(facing)
        com()
        status = com.outputs[-1]

        area = updatemap(area, x, y, facing, status)

        if status == GOAL: return area

        x, y = explore(area, x, y)

        draw(area)

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __add__(self, other):
        return Point(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return Point(self.x - other.x, self.y - other.y)

neighboor = [
    Point(1, 0),   # north
    Point(-1, 0),  # south
    Point(0, -1),  # west
    Point(0, 1),   # east
]

def findgoal(com):
    curr    = Point(0,0)
    visited = {curr : FREE}
    facing  = NORTH

    while True:
        facing = random.choice(range(4))
        while visited.get(curr + neighboor[facing], FREE) == WALL:
            facing = random.choice(range(4))

        com.update([facing])
        com()
        status = com.last

        if status == GOAL:
            visited[curr + neighboor[facing]] = GOAL
            break

        if status == WALL:
            visited[curr + neighboor[facing]] = WALL

        if status == MOVED:
            curr += neighboor[facing]
            visited[curr] = FREE

    return visited

if __name__ == '__main__':
    tape = parse('inputs/day15.txt')
    com = computer('repair', tape, [1])()

    area = findgoal(com)
    print(area)
    print('Part 1: {}'.format(comp1.outputs[0]))
    print('Part 2: {}'.format(comp2.outputs[0]))
