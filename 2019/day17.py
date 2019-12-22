import logging
from collections import deque
import numpy as np

def parse(path):
    with open(path, mode='r') as f:
        return [int(x) for x in f.readline().split(',')]

class computer:
    def __init__(self, name, program, inputs=None):
        self.name    = name
        self.program = list(program)
        self.ip      = 0
        self.base    = 0
        self.outputs = []

        if inputs is None: inputs = []
        self.inputs  = deque(inputs)

        self.pause   = True

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

LEFT =0
RIGHT=1
UP=3
DOWN=4

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
    intcodes = parse('inputs/day17.txt')
    com = computer('ascii', intcodes).run()

    area = [str(chr(x)) for x in com.outputs]
    print('Part 1: {}'.format(alignment(list(area))))

    route = path(area)

    # Although a bit cheaty: manually map out the patterns, resulted in:
    main = ascii_seq('A,C,A,C,B,B,C,A,B,A')
    A = ascii_seq(','.join(route[:8]))
    B = ascii_seq(','.join(route[8:14]))
    C = ascii_seq(','.join(route[28:34]))

    instructions = main + A + B + C + [110, 10]

    intcodes[0] = 2
    com = computer('ascii', intcodes, instructions)
    com.run()

    print('Part 2: {}'.format(com.outputs[-1]))
