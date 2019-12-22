import logging

from itertools import permutations
from collections import deque

def parse(path):
    with open(path, mode='r') as f:
        return [int(x) for x in f.readline().split(',')]

class computer:
    def __init__(self, program, inputs):
        self.program = list(program)
        self.ip      = 0
        self.outputs = []
        self.inputs  = deque(inputs)
        self.paused  = False

        ext = [0] * 1000000
        self.program.extend(ext)

    def run(self):
        self.paused = False
        opcode = None

        while opcode != 99 and not self.paused:
            opcode, c, b, a = self.instruction()
            if   opcode == 1: self.add(c, b, a)
            elif opcode == 2: self.mul(c, b, a)
            elif opcode == 3: self.put()
            elif opcode == 4: self.get(c)
            elif opcode == 5: self.jumpt(c, b)
            elif opcode == 6: self.jumpf(c, b)
            elif opcode == 7: self.less(c, b, a)
            elif opcode == 8: self.equal(c, b, a)
            else:
                break
        return self

    def instruction(self):
        opcode = 10*((self.program[self.ip] // 10) % 10) + self.program[self.ip] % 10
        c = (self.program[self.ip] // 100)  % 10
        b = (self.program[self.ip] // 1000) % 10
        a = (self.program[self.ip] // 10000)

        if opcode == 99: return opcode, c, b, a

        if   c == 0: c = self.program[self.program[self.ip + 1]]
        elif c == 1: c = self.program[self.ip + 1]

        if   b == 0: b = self.program[self.program[self.ip + 2] ]
        elif b == 1: b = self.program[self.ip + 2]

        if   a == 0: a = self.program[self.ip + 3]
        elif a == 1: a = self.program[self.ip + 3]

        return opcode, c, b, a

    def add(self, c, b, a):
        self.program[a] = c + b
        self.ip += 4

    def mul(self, c, b, a):
        self.program[a] = c * b
        self.ip += 4

    def put(self):
        if len(self.inputs) == 0:
            self.paused = True
            return

        addr = self.program[self.ip + 1]
        self.program[ addr ] = self.inputs.popleft()
        self.ip += 2

    def get(self, c):
        self.outputs.append(c)
        self.ip += 2

    def jumpt(self, c, b):
        if c != 0: self.ip  = b
        else:      self.ip += 3

    def jumpf(self, c, b):
        if c == 0: self.ip  = b
        else:      self.ip += 3

    def less(self, c, b, a):
        if c < b: self.program[a] = 1
        else:     self.program[a] = 0
        self.ip += 4

    def equal(self, c, b, a):
        if c == b: self.program[a] = 1
        else:      self.program[a] = 0
        self.ip += 4

def part1(program, testid=0):
    out = float('-inf')
    for a,b,c,d,e in permutations(range(5)):
        amp_a = computer(program,[a, testid])
        amp_a.run()
        amp_b = computer(program,[b, amp_a.outputs[0]])
        amp_b.run()
        amp_c = computer(program,[c, amp_b.outputs[0]])
        amp_c.run()
        amp_d = computer(program,[d, amp_c.outputs[0]])
        amp_d.run()
        amp_e = computer(program,[e, amp_d.outputs[0]])
        amp_e.run()
        output = amp_e.outputs[0]
        if output > out: out = output
    return out

def part2(program, init=0):
    outputs = []
    for inputs in permutations(range(5, 10)):
        amps = [computer(program, [x]).run() for x in inputs]
        out  = init
        halted = False

        while not halted:
            for amp in amps:
                amp.inputs.append(out)
                amp.run()
                out = amp.outputs[-1]

                if amp.paused: continue

                halted = True

            outputs.append(amps[-1].outputs[-1])

    return max(outputs)

if __name__ == '__main__':
    program = parse('inputs/day07.txt')

    print('Part 1: {}'.format(part1(program)))
    print('Part 2: {}'.format(part2(program)))
