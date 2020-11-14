from os import system
from sys import stdout
from collections import deque

from . import helpers

import numpy as np

def parse(path):
    with open(path, mode='r') as f:
        return [int(x) for x in f.readline().split(',')]

EMPTY  = 0
WALL   = 1
BLOCK  = 2
PADDLE = 3
BALL   = 4

STAY  = 0
LEFT  = -1
RIGHT = 1

def blocks(a):
    n = 0
    for line in a:
        for item in line:
            if item != BLOCK: continue
            n += 1
    return n

def find(a, what=BALL):
    for x, line in enumerate(a):
        for y, item in enumerate(line):
            if item != what: continue
            return  y, x

def score(a, points=0):
    for x, y, item in zip(a[0::3], a[1::3], a[2::3]):
        if x == -1 and y == 0: return item
    return points

def empty(a):
    sizex = max([x for x in a[0::3]]) + 1
    sizey = max([x for x in a[1::3]]) + 1

    grid = np.zeros(sizex * sizey)
    grid = np.reshape(grid, (sizey, sizex))
    return grid

def update(grid, a):
    for x, y, item in zip(a[0::3], a[1::3], a[2::3]):

        if   item == WALL:   grid[y][x] = WALL
        elif item == BLOCK:  grid[y][x] = BLOCK
        elif item == BALL:   grid[y][x] = BALL
        elif item == PADDLE: grid[y][x] = PADDLE
        else:                grid[y][x] = EMPTY

    return grid

def plot(grid, points):
    system('clear')
    output = []
    for line in grid:
        for item in line:
            if   item == EMPTY:  output.append(' ')
            elif item == WALL:   output.append('#')
            elif item == BLOCK:  output.append('*')
            elif item == BALL:   output.append('0')
            elif item == PADDLE: output.append('=')
            output.append(' ')
        output.append('\n')
    output.append('\n')
    output.append('Points: {}\n'.format(points))
    stdout.write(''.join(output))

def play(com):
    joystick = STAY
    com.update([joystick])
    com()

    grid = update(empty(com.out), com.out)

    points = score(com.out, 0)
    com.outputs = []
    plot(grid, points)
    while blocks(grid) > 0:
        paddle = find(grid, PADDLE)
        ball   = find(grid, BALL)

        if ball[1] >= paddle[1]: break

        if   ball[0] == paddle[0]: joystick = STAY
        elif ball[0] <  paddle[0]: joystick = LEFT
        elif ball[0] >  paddle[0]: joystick = RIGHT
        else: pass

        com.update([joystick])
        com()

        points = score(com.outputs, points)

        grid = update(grid, com.outputs)
        plot(grid, points)

        com.outputs = []

    return score(com.out, points)

def puzzle13(path='inputs/day13.txt'):
    tape = parse(path)

    comp1 = helpers.computer('arcade', tape, [])()
    grid = update(empty(comp1.out), comp1.out)

    part1 = blocks(grid)

    tape[0] = 2
    comp2 = helpers.computer('arcade', tape, [])

    part2 = play(comp2)

    system('clear')
    return part1, part2
