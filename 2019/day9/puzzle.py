"""--- Day 9: Sensor Boost ---

You've just said goodbye to the rebooted rover and left Mars when you receive a
faint distress signal coming from the asteroid belt. It must be the Ceres
monitoring station!

In order to lock on to the signal, you'll need to boost your sensors. The Elves
send up the latest BOOST program - Basic Operation Of System Test.

While BOOST (your puzzle input) is capable of boosting your sensors, for
tenuous safety reasons, it refuses to do so until the computer it runs on
passes some checks to demonstrate it is a complete Intcode computer.

Your existing Intcode computer is missing one key feature: it needs support for
parameters in relative mode.

Parameters in mode 2, relative mode, behave very similarly to parameters in
position mode: the parameter is interpreted as a position. Like position mode,
parameters in relative mode can be read from or written to.

The important difference is that relative mode parameters don't count from
address 0. Instead, they count from a value called the relative base. The
relative base starts at 0.

The address a relative mode parameter refers to is itself plus the current
relative base. When the relative base is 0, relative mode parameters and
position mode parameters with the same value refer to the same address.

For example, given a relative base of 50, a relative mode parameter of -7
refers to memory address 50 + -7 = 43.

The relative base is modified with the relative base offset instruction:

Opcode 9 adjusts the relative base by the value of its only parameter. The
relative base increases (or decreases, if the value is negative) by the value
of the parameter.  For example, if the relative base is 2000, then after the
instruction 109,19, the relative base would be 2019. If the next instruction
were 204,-34, then the value at address 1985 would be output.

Your Intcode computer will also need a few other capabilities:

The computer's available memory should be much larger than the initial program.
Memory beyond the initial program starts with the value 0 and can be read or
written like any other memory. (It is invalid to try to access memory at a
negative address, though.) The computer should have support for large numbers.
Some instructions near the beginning of the BOOST program will verify this
capability.

Here are some example programs that use these features:

 - 109,1,204,-1,1001,100,1,100,1008,100,16,101,1006,101,0,99 takes no input and
   produces a copy of itself as output.
 - 1102,34915192,34915192,7,4,7,99,0 should output a 16-digit number.
 - 104,1125899906842624,99 should output the large number in the middle.

The BOOST program will ask for a single input; run it in test mode by providing
it the value 1. It will perform a series of checks on each opcode, output any
opcodes (and the associated parameter modes) that seem to be functioning
incorrectly, and finally output a BOOST keycode.

Once your Intcode computer is fully functional, the BOOST program should report
no malfunctioning opcodes when run in test mode; it should only output a single
value, the BOOST keycode. What BOOST keycode does it produce?
"""
import logging
from collections import deque

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

if __name__ == '__main__':
    intcodes = parse('input.txt')
    comp1 = computer('Computer 1', intcodes, [1]).run()
    comp2 = computer('Computer 1', intcodes, [2]).run()

    print('Part 1: {}'.format(comp1.outputs[0]))
    print('Part 2: {}'.format(comp2.outputs[0]))
