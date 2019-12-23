import logging
import numpy as np

from collections import deque

def parse(path):
    with open(path, mode='r') as f:
        return [int(x) for x in f.readline().split(',')]

class computer:
    def __init__(self, name, tape, inputs):
        self.name    = name
        self.tape    = list(tape)
        self.ip      = 0
        self.base    = 0
        self.outputs = []
        self.inputs  = deque(inputs)

        self.running = False

        ext = [0] * 10000
        self.tape.extend(ext)

    def __call__(self):
        self.running = True
        opcode       = None

        while opcode != 99 and self.running:
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

    def reset(self, a=None):
        self.tape    = list(tape)
        self.ip      = 0
        self.base    = 0
        self.outputs = []
        self.inputs  = deque(inputs) if a is None else []

    def update(self, a):
        self.inputs.extend(a)

    @property
    def out(self):
        return self.outputs

    @property
    def last(self):
        return self.outputs[-1]

    @property
    def first(self):
        return self.outputs[0]

    def instruction(self):
        opcode = self.tape[self.ip] % 100
        c = (self.tape[self.ip] // 100)  % 10
        b = (self.tape[self.ip] // 1000) % 10
        a = (self.tape[self.ip] // 10000)

        if opcode == 99: return opcode, c, b, a

        if   c == 0: c = self.tape[self.ip + 1]
        elif c == 1: c = self.ip + 1
        elif c == 2: c = self.tape[self.ip + 1] + self.base

        if   b == 0: b = self.tape[self.ip + 2]
        elif b == 1: b = self.ip + 2
        elif b == 2: b = self.tape[self.ip + 2] + self.base

        if   a == 0: a = self.tape[self.ip + 3]
        elif a == 1: a = self.tape[self.ip + 3]
        elif a == 2: a = self.tape[self.ip + 3] + self.base

        return opcode, c, b, a

    def add(self, c, b, a):
        self.tape[a] = self.tape[c] + self.tape[b]
        self.ip += 4

    def mul(self, c, b, a):
        self.tape[a] = self.tape[c] * self.tape[b]
        self.ip += 4

    def put(self, c):
        if len(self.inputs) == 0:
            self.running = False
            return

        self.tape[c] = self.inputs.popleft()
        self.ip += 2

    def get(self, c):
        self.outputs.append(self.tape[c])
        self.ip += 2

    def jumpt(self, c, b):
        if self.tape[c] != 0: self.ip  = self.tape[b]
        else:                 self.ip += 3

    def jumpf(self, c, b):
        if self.tape[c] == 0: self.ip = self.tape[b]
        else:                 self.ip += 3

    def less(self, c, b, a):
        if self.tape[c] < self.tape[b]: self.tape[a] = 1
        else:                           self.tape[a] = 0
        self.ip += 4

    def equal(self, c, b, a):
        if self.tape[c] == self.tape[b]: self.tape[a] = 1
        else:                            self.tape[a] = 0
        self.ip += 4

    def rbase(self, c):
        self.base += self.tape[c]
        self.ip += 2
