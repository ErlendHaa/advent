from collections import deque
from collections import defaultdict
from os import system
from time import sleep

from . import helpers

import numpy as np

def parse(path):
    with open(path, mode='r') as f:
        return [int(x) for x in f.readline().split(',')]

BLACK, WHITE = 0, 1
LEFT,RIGHT, UP, DOWN = 0, 1, 3, 4

roadrules = {
    (UP,    LEFT)  : LEFT,
    (UP,    RIGHT) : RIGHT,
    (DOWN,  LEFT)  : RIGHT,
    (DOWN,  RIGHT) : LEFT,
    (LEFT,  LEFT)  : DOWN,
    (LEFT,  RIGHT) : UP,
    (RIGHT, LEFT)  : UP,
    (RIGHT, RIGHT) : DOWN,
}

def move(turn, x, y, curdir):
    newdir = roadrules[(curdir, turn)]

    if   newdir == LEFT:  x -= 1
    elif newdir == RIGHT: x += 1
    elif newdir == UP:    y -= 1
    elif newdir == DOWN:  y += 1

    return x, y, newdir

def draw(area):
    out = []

    area = area[:40,:6]
    for x, line in enumerate(area.T):
        for y, point in enumerate(line):
            if   point == WHITE: out.append('#')
            elif point == BLACK: out.append(' ')
        out.append('\n')
    out.append('\n')
    print(''.join(out))

def paint(com, start_on=BLACK):
    x, y = 0,0
    facing = UP

    painted = set()
    area = np.reshape(np.zeros(10000), (100, 100))

    area[x,y] = start_on
    while not com.running:
        cur_color = area[x][y]

        com.update([cur_color])
        com()

        paint_color, turn = com.out[-2:]

        if paint_color != cur_color:
            painted.add((x,y))
            area[x, y] = paint_color

        x, y, facing = move(turn, x, y, facing)

    return len(painted), area

def puzzle11(path='inputs/day11.txt'):
    intcodes = parse(path)
    com = helpers.computer('painter', intcodes, [])

    painted, _ = paint(com)

    com = helpers.computer('painter', intcodes, [])
    _, area = paint(com, start_on=WHITE)

    draw(area)
    return painted, 'see plot'
