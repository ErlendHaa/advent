import copy

from .computer import parse_instructions, Computer

def find_infinite_loop(computer):
    seen = set()
    while computer.peek_next() not in seen:
        seen.add(computer.peek_next())
        computer.execute()

    return computer.accumulator

def swap(instructions, i):
    instructions = copy.deepcopy(instructions)
    if instructions[i].name == 'nop': instructions[i].name = 'jmp'
    if instructions[i].name == 'jmp': instructions[i].name = 'nop'
    return instructions

def repair(instructions):
    for i, inst in enumerate(instructions):
        if inst.name != 'jmp' and inst.name != 'nop': continue

        computer = Computer( swap(instructions, i) )
        try:             find_infinite_loop(computer)
        except EOFError: return computer.accumulator # No loop

def puzzle8(path='inputs/day08.txt'):
    instructions = parse_instructions(path)
    computer = Computer(instructions)

    part1 = find_infinite_loop(computer)
    part2 = repair(instructions)

    return part1, part2
