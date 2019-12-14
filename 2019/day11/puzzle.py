from collections import deque
from collections import defaultdict
from os import system
from time import sleep

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
        self.paused = True

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

BLACK=0
WHITE=1

LEFT =0
RIGHT=1
UP=3
DOWN=4

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
    while com.paused:
        cur_color = area[x][y]

        com.inputs.append(cur_color)
        com.run()

        paint_color, turn = com.outputs[-2:]

        if paint_color != cur_color:
            painted.add((x,y))
            area[x, y] = paint_color

        x, y, facing = move(turn, x, y, facing)

    return len(painted), area

if __name__ == '__main__':
    intcodes = parse('input.txt')
    com = computer('painter', intcodes, [])

    painted, _ = paint(com)

    com = computer('painter', intcodes, [])
    _, area = paint(com, start_on=WHITE)

    print('Part 1: {}'.format(painted))
    print('Part 2:')
    draw(area)
