"""--- Day 7: Amplification Circuit ---

Based on the navigational maps, you're going to need to send more power to your
ship's thrusters to reach Santa in time. To do this, you'll need to configure a
series of amplifiers already installed on the ship.

There are five amplifiers connected in series; each one receives an input
signal and produces an output signal. They are connected such that the first
amplifier's output leads to the second amplifier's input, the second
amplifier's output leads to the third amplifier's input, and so on. The first
amplifier's input value is 0, and the last amplifier's output leads to your
ship's thrusters.

    O-------O  O-------O  O-------O  O-------O  O-------O
0 ->| Amp A |->| Amp B |->| Amp C |->| Amp D |->| Amp E |-> (to thrusters)
    O-------O  O-------O  O-------O  O-------O  O-------O

The Elves have sent you some Amplifier Controller Software (your puzzle input),
a program that should run on your existing Intcode computer. Each amplifier
will need to run a copy of the program.

When a copy of the program starts running on an amplifier, it will first use an
input instruction to ask the amplifier for its current phase setting (an
integer from 0 to 4). Each phase setting is used exactly once, but the Elves
can't remember which amplifier needs which phase setting.

The program will then call another input instruction to get the amplifier's
input signal, compute the correct output signal, and supply it back to the
amplifier with an output instruction. (If the amplifier has not yet received an
input signal, it waits until one arrives.)

Your job is to find the largest output signal that can be sent to the thrusters
by trying every possible combination of phase settings on the amplifiers. Make
sure that memory is not shared or reused between copies of the program.

For example, suppose you want to try the phase setting sequence 3,1,2,4,0,
which would mean setting amplifier A to phase setting 3, amplifier B to setting
1, C to 2, D to 4, and E to 0. Then, you could determine the output signal that
gets sent from amplifier E to the thrusters with the following steps:

 - Start the copy of the amplifier controller software that will run on
   amplifier A. At its first input instruction, provide it the amplifier's phase
   setting, 3. At its second input instruction, provide it the input signal, 0.
   After some calculations, it will use an output instruction to indicate the
   amplifier's output signal.
 - Start the software for amplifier B. Provide it the phase setting (1) and
   then whatever output signal was produced from amplifier A. It will then produce
   a new output signal destined for amplifier C.
 - Start the software for amplifier C, provide the phase setting (2) and the
   value from amplifier B, then collect its output signal.
 - Run amplifier D's software, provide the phase setting (4) and input value,
   and collect its output signal.
 - Run amplifier E's software, provide the phase setting (0) and input value,
   and collect its output signal.
 - The final output signal from amplifier E would be sent to the thrusters.
   However, this phase setting sequence may not have been the best one; another
   sequence might have sent a higher signal to the thrusters.

Here are some example programs:

Max thruster signal 43210 (from phase setting sequence 4,3,2,1,0):

3,15,3,16,1002,16,10,16,1,16,15,15,4,15,99,0,0
Max thruster signal 54321 (from phase setting sequence 0,1,2,3,4):

3,23,3,24,1002,24,10,24,1002,23,-1,23,
101,5,23,23,1,24,23,23,4,23,99,0,0
Max thruster signal 65210 (from phase setting sequence 1,0,4,3,2):

3,31,3,32,1002,32,10,32,1001,31,-2,31,1007,31,0,33,
1002,33,7,33,1,33,31,31,1,32,31,31,4,31,99,0,0,

Try every combination of phase settings on the amplifiers. What is the highest
signal that can be sent to the thrusters?"""
import logging
import itertools

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
    for a,b,c,d,e in itertools.permutations(range(5)):
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
    for inputs in itertools.permutations(range(5, 10)):
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
    program = parse('input.txt')

    print('Part 1: {}'.format(part1(program)))
    print('Part 2: {}'.format(part2(program)))
