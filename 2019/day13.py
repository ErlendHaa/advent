from os import system
from sys import stdout
from collections import deque

import numpy as np

def parse(path):
    with open(path, mode='r') as f:
        return [int(x) for x in f.readline().split(',')]

class computer:
    def __init__(self, name, program, inputs):
        self.name    = name
        self.program = list(program)
        self.ip      = 0
        self.base    = 0
        self.outputs = []
        self.inputs  = deque(inputs)

        ext = [0] * 1000000
        self.program.extend(ext)

    def run(self):
        self.paused = False
        opcode      = None

        while opcode != 99 and not self.paused:
            opcode, c, b, a = self.instruction()
            if   opcode == 1: self.add(c, b, a)
            elif opcode == 2: self.mul(c, b, a)
            elif opcode == 3: self.put(c)
            elif opcode == 4: self.get(c)
            elif opcode == 5: self.jumpt(c, b)
            elif opcode == 6: self.jumpf(c, b)
            elif opcode == 7: self.less(c, b, a)
            elif opcode == 8: self.equal(c, b, a)
            elif opcode == 9: self.rbase(c)
            else:
                break
        return self

    def instruction(self):
        opcode = self.program[self.ip] % 100
        c = (self.program[self.ip] // 100)  % 10
        b = (self.program[self.ip] // 1000) % 10
        a = (self.program[self.ip] // 10000)

        if opcode == 99: return opcode, c, b, a

        if   c == 0: c = self.program[self.ip + 1]
        elif c == 1: c = self.ip + 1
        elif c == 2: c = self.program[self.ip + 1] + self.base

        if   b == 0: b = self.program[self.ip + 2]
        elif b == 1: b = self.ip + 2
        elif b == 2: b = self.program[self.ip + 2] + self.base

        if   a == 0: a = self.program[self.ip + 3]
        elif a == 1: a = self.program[self.ip + 3]
        elif a == 2: a = self.program[self.ip + 3] + self.base

        return opcode, c, b, a

    def add(self, c, b, a):
        self.program[a] = self.program[c] + self.program[b]
        self.ip += 4

    def mul(self, c, b, a):
        self.program[a] = self.program[c] * self.program[b]
        self.ip += 4

    def put(self, c):
        if len(self.inputs) == 0:
            self.paused = True
            return

        self.program[c] = self.inputs.popleft()
        self.ip += 2

    def get(self, c):
        self.outputs.append(self.program[c])
        self.ip += 2

    def jumpt(self, c, b):
        if self.program[c] != 0: self.ip  = self.program[b]
        else:                    self.ip += 3

    def jumpf(self, c, b):
        if self.program[c] == 0: self.ip = self.program[b]
        else:                    self.ip += 3

    def less(self, c, b, a):
        if self.program[c] < self.program[b]: self.program[a] = 1
        else:                                 self.program[a] = 0
        self.ip += 4

    def equal(self, c, b, a):
        if self.program[c] == self.program[b]: self.program[a] = 1
        else:                                  self.program[a] = 0
        self.ip += 4

    def rbase(self, c):
        self.base += self.program[c]
        self.ip += 2


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

def play(comp):
    joystick = STAY
    comp.inputs.append(joystick)
    comp.run()

    grid = update(empty(comp.outputs), comp.outputs)

    points = score(comp.outputs, 0)
    comp.outputs = []
    plot(grid, points)
    while blocks(grid) > 0:
        paddle = find(grid, PADDLE)
        ball   = find(grid, BALL)

        if ball[1] >= paddle[1]: break

        if   ball[0] == paddle[0]: joystick = STAY
        elif ball[0] <  paddle[0]: joystick = LEFT
        elif ball[0] >  paddle[0]: joystick = RIGHT
        else: pass

        comp.inputs.append(joystick)
        comp.run()

        points = score(comp.outputs, points)

        grid = update(grid, comp.outputs)
        plot(grid, points)

        comp.outputs = []

    return score(comp.outputs, points)

if __name__ == '__main__':
    intcodes = parse('inputs/day13.txt')

    comp1 = computer('arcade', intcodes, []).run()
    grid = update(empty(comp1.outputs), comp1.outputs)

    part1 = blocks(grid)

    intcodes[0] = 2
    comp2 = computer('arcade', intcodes, [])

    part2 = play(comp2)

    print('Part 1: {}'.format(part1))
    print('Part 2: {}'.format(part2))
