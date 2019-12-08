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

class amp:
    def __init__(self, name, program, phase):
        self.program = list(program)
        self.name    = name
        self.inputs  = deque()
        self.phase   = phase
        self.output  = []
        self.ip      = 0

    def __repr__(self):
        return self.name

    def putin(self, value):
        self.inputs = deque([value])

    def popin(self):
        return self.inputs.popleft()

    def popout(self):
        out = self.output
        self.output = []
        return out

    def run(self):
        opcode = 0
        while opcode != 99:
            opcode, C, B, A = instruction( self.program, self.ip )
            if   opcode == 1:
                self.ip = add(self.program, self.ip, C, B, A)
            elif opcode == 2:
                self.ip = mul(self.program, self.ip, C, B, A)
            elif opcode == 3:
                inp = self.inputs.popleft()
                self.ip = put(self.program, self.ip, inp )
            elif opcode == 4:
                self.ip, out = get(self.program, self.ip)
                yield out
            elif opcode == 5:
                self.ip = jumpt(program, self.ip, C, B)
            elif opcode == 6:
                self.ip = jumpf(program, self.ip, C, B)
            elif opcode == 7:
                self.ip = less( self.program, self.ip, C, B, A)
            elif opcode == 8:
                self.ip = equal(program, self.ip, C, B, A)
            else:
                msg = 'Something went wrong in amp {}, found value {} in address {}, current output {}'
                logging.warning(msg.format(self.name, opcode, self.ip,
                    self.output))
                raise
        raise StopIteration

def feedback(program, inputs, init=0):
    a, b, c, d, e = tuple(inputs)
    A = amp('a', program, phase=a)
    B = amp('b', program, phase=b)
    C = amp('c', program, phase=c)
    D = amp('d', program, phase=d)
    E = amp('e', program, phase=e)

    output = []
    amps = deque([A, B, C, D, E])
    value = init
    while amps:
        cur = amps.popleft()
        cur.putin(value)
        try:
            value = next(cur.run())
            amps.append(cur)
        except StopIteration:
            break

    return value

def run(program, inputs):
    ip, pin = 0, 0
    output = []

    while True:
        opcode, C, B, A = instruction( program, ip )
        if   opcode == 1: ip = add(  program, ip, C, B, A)
        elif opcode == 2: ip = mul(  program, ip, C, B, A)
        elif opcode == 4: ip, output = get(  program, ip)
        elif opcode == 5: ip = jumpt(program, ip, C, B)
        elif opcode == 6: ip = jumpf(program, ip, C, B)
        elif opcode == 7: ip = less( program, ip, C, B, A)
        elif opcode == 8: ip = equal(program, ip, C, B, A)
        elif opcode == 3:
            ip = put(  program, ip, inputs[pin])
            pin += 1
        elif opcode == 99:
            msg = 'Program finished with code 99, output: {}'
            logging.warning(msg.format(output[0]))
            break
        else:
            break

    return output

def instruction(program, ip):
    opcode, A, B, C = 0, 0, 0, 0
    inst = [int(x) for x in str(program[ip])]
    opcode = inst[-1]

    try: C = inst[-3]
    except: pass

    try: B = inst[-4]
    except: pass

    try: A = inst[-5]
    except: pass

    try:
        if C == 0: C = program[ program[ip + 1] ]
        else:      C = program[ ip + 1]
    except: pass

    try:
        if B == 0: B = program[ program[ip + 2] ]
        else:      B = program[ ip + 2]
    except: pass

    try:
        if A == 0: A = program[ip + 3]
        else:      A = ip + 3
    except: pass

    return opcode, C, B, A


def add(program, ip, c, b, a):
    program[a] = c + b
    return ip + 4

def mul(program, ip, c, b, a):
    program[a] = c * b
    return ip + 4

def put(program, ip, val):
    program[ program[ ip + 1] ] = val
    return ip + 2

def get(program, ip):
    val = program[ program[ ip + 1] ]
    return ip + 2, val

def jumpt(program, ip, c, b):
    if c != 0: return  b
    else:      return ip + 3

def jumpf(program, ip, c, b):
    if c == 0: return b
    else:      return ip + 3

def less(program, ip, c, b, a):
    if c < b: program[a] = 1
    else:     program[a] = 0
    return ip + 4

def equal(program, ip, c, b, a):
    if c == b: program[a] = 1
    else:      program[a] = 0
    return ip + 4

def amplifiers(program, inputs, testid=0):
    a, b, c, d, e = tuple(inputs)
    return output

def part1(program, testid=0):
    out = float('-inf')
    for a,b,c,d,e in itertools.permutations(range(5)):
        output = run(program,[a, testid])
        output = run(program,[b, output])
        output = run(program,[c, output])
        output = run(program,[d, output])
        output = run(program,[e, output])
        if output > out: out = output
    return out

def part2(program):
    outputs = []
    for inputs in itertools.permutations(range(5, 10)):
        out = feedback(program, inputs)
        outputs.append(out)
    return outputs

if __name__ == '__main__':
    program = parse('input.txt')
    print('Part 1: {}'.format(part1(program)))

    program = [3,26,1001,26,-4,26,3,27,1002,27,2,27,1,27,26,
            27,4,27,1001,28,-1,28,1005,28,6,99,0,0,5]
    program =[
            3,52,1001,52,-5,52,3,53,1,52,56,54,1007,54,5,55,1005,55,26,1001,54,
            -5,54,1105,1,12,1,53,54,53,1008,54,0,55,1001,55,1,55,2,53,55,53,4,
            53,1001,56,-1,56,1005,56,6,99,0,0,0,0,10]

    #print('Part 2: {}'.format(part2(program)))
