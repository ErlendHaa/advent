


def parse_instructions(path):
    instructions = []
    with open(path) as f:
        for line in f.readlines():
            line = line.split(' ')
            instruction = Instruction(line[0], [int(x) for x in line[1:]])
            instructions.append(instruction)

    return instructions


class Instruction:
    def __init__(self, name, args):
        self.name = name
        self.args = args

    def __repr__(self):
        return "Instruction({}, {})".format(self.name, self.args)

class Computer:
    def __init__(self, instructions, acc=0, pc=0):
        self.instructions = instructions
        self.accumulator  = acc
        self.pc           = pc

    def reset(self, acc=0, pc=0):
        self.accumulator = acc
        self.pc = pc

    def peek_next(self):
        if self.pc == len(self.instructions):
            raise EOFError('End of instruction set')
        return self.instructions[self.pc]

    def execute(self):
        instruction = self.peek_next()
        if   instruction.name == 'jmp': return self.jmp()
        elif instruction.name == 'nop': return self.nop()
        elif instruction.name == 'acc': return self.acc()
        else:
            msg = "invalid instruction ({}) at pos {}"
            raise ValueError(msg.format(instruction.id, self.pc))

    def increment(self):
        self.pc += 1
        return self

    def jmp(self):
        self.pc += self.instructions[self.pc].args[0]
        return self

    def nop(self):
        return self.increment()

    def acc(self):
        self.accumulator += self.instructions[self.pc].args[0]
        return self.increment()
