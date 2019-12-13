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

BLACK=1
WHITE=0

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

def move(turn, curpos, curdir):
    newdir = roadrules[(curdir, turn)]

    curpos = list(curpos)
    if   newdir == LEFT:  curpos[0] -= 1
    elif newdir == RIGHT: curpos[0] += 1
    elif newdir == UP:    curpos[1] += 1
    elif newdir == DOWN:  curpos[1] += 1

    return tuple(curpos), newdir

def draw(area, pos, direction):
    out = []
    for x, line in enumerate(area):
        for y, point in enumerate(line):
            if x == pos[0] and y == pos[1]:
                if direction == UP: out.append('^')
                if direction == DOWN: out.append('v')
                if direction == RIGHT: out.append('>')
                if direction == LEFT: out.append('<')
            elif point == WHITE: out.append(' ')
            elif point == BLACK: out.append('#')
            out.append(' ')
        out.append('\n')
    out.append('\n')

    system('clear')
    print(''.join(out))

def empty(x=30, y=50):
    area = np.reshape(np.zeros(x*y), (x,y))
    area[0]  = np.ones(y)
    area[-1] = np.ones(y)
    area[:, 0] = 1
    area[:,-1] = 1
    return area

def paint(com):
    cur_pos   = (10,5)
    cur_dir   = UP
    cur_color = BLACK
    painted = defaultdict(lambda:BLACK)
    area = empty()
    com.paused = True
    while com.paused:
        com.inputs.append(cur_color)
        com.run()

        draw(area, cur_pos, cur_dir)

        paint_color, turn = com.outputs[-2:]

        if paint_color != cur_color:
            painted[cur_pos] = paint_color
            area[cur_pos[0]][cur_pos[1]] = paint_color

        cur_pos, cur_dir = move(turn, cur_pos, cur_dir)

        if cur_pos in painted: cur_color = painted[cur_pos]
        else:                  cur_color = BLACK
        sleep(1)
    return painted

if __name__ == '__main__':
    intcodes = parse('input.txt')
    com = computer('painter', intcodes, [BLACK])

    area = paint(com)
    print('Part 1: {}'.format(len(area)))
