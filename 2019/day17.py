import logging
import numpy as np

from intcode import computer
from collections import deque

LEFT, RIGHT, UP, DOWN = 0, 1, 3, 4

def parse(path):
    with open(path, mode='r') as f:
        return [int(x) for x in f.readline().split(',')]

def alignment(area):
    char = ''
    llen = 0
    while char != '\n':
        llen += 1
        char = area[llen]

    area = list(filter(lambda x: x != '\n', area))
    area = np.reshape(np.array(area), (llen, llen))

    parameters = []
    for x, line in enumerate(area):
        for y, char in enumerate(line):
            if char != '#': continue
            try:
                if area[x, y-1] != '#': continue
                if area[x, y+1] != '#': continue
                if area[x+1, y] != '#': continue
                if area[x-1, y] != '#': continue
            except IndexError:
                # On an edge, not intersections here so just continue
                continue
            parameters.append(x*y)
    return sum(parameters)

def forward(area, curr, facing):
    move = False
    x, y = curr

    def index(x, y):
        try:
            return area[x, y] == '#'
        except:
            return False

    if facing == UP    and index(x - 1, y):
        move = True
        x -= 1
    if facing == DOWN  and index(x + 1, y):
        move = True
        x += 1
    if facing == RIGHT and index(x, y + 1):
        move = True
        y += 1
    if facing == LEFT  and index(x, y - 1):
        move = True
        y -= 1

    curr = (x, y)
    return move, curr

def newdir(area, curr, facing):
    x, y = curr
    def index(x, y):
        try:
            return area[x, y] == '#'
        except:
            return False

    if facing == UP and index(x, y-1): return 'L', LEFT
    if facing == UP and index(x, y+1): return 'R', RIGHT

    if facing == DOWN and index(x, y+1): return 'L', RIGHT
    if facing == DOWN and index(x, y-1): return 'R', LEFT

    if facing == LEFT and index(x+1, y): return 'L', DOWN
    if facing == LEFT and index(x-1, y): return 'R', UP

    if facing == RIGHT and index(x-1, y): return 'L', UP
    if facing == RIGHT and index(x+1, y): return 'R', DOWN

    return None, None

def path(area):
    area = list(filter(lambda x: x != '\n', area))
    area = np.reshape(np.array(area), (57, 57))

    curr = None
    facing = UP

    for x, line in enumerate(area):
        for y, char in enumerate(line):
            if char != '^': continue
            curr = (x, y)
            break

    route = []
    while True:
        turn, facing = newdir(area, curr, facing)
        if turn == None: break
        route.append(turn)

        lenght = 0
        move, curr = forward(area, curr, facing)
        while move:
            move, curr = forward(area, curr, facing)
            lenght += 1

        route.append(str(lenght))

    return route

def ascii_seq(a):
    a = [ord(x) for x in a]
    a.append(10)
    return a

if __name__ == '__main__':
    tape = parse('inputs/day17.txt')
    com = computer('ascii', tape, [])()

    area = [str(chr(x)) for x in com.out]
    print('Part 1: {}'.format(alignment(list(area))))

    route = path(area)

    # Although a bit cheaty: manually map out the patterns, resulted in:
    main = ascii_seq('A,C,A,C,B,B,C,A,B,A')
    A = ascii_seq(','.join(route[:8]))
    B = ascii_seq(','.join(route[8:14]))
    C = ascii_seq(','.join(route[28:34]))

    instructions = main + A + B + C + [110, 10]

    tape[0] = 2
    com = computer('ascii', tape, instructions)
    com()

    print('Part 2: {}'.format(com.last))
