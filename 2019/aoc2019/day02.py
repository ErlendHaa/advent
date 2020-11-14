from itertools import product

def parse(path):
    with open(path, mode='r') as f:
        return list(map(int, f.readline().split(',')))

def run(program, noun, verb):
    ip = 0;
    program[1] = noun
    program[2] = verb

    while True:
        value = program[ip]

        if   value == 1:  sum(program, ip)
        elif value == 2:  mul(program, ip)
        elif value == 99: break
        ip += 4

    return program

def sum(program, cur):
    idx1 = program[cur + 1]
    idx2 = program[cur + 2]
    idx3 = program[cur + 3]

    program[idx3] = program[idx1] + program[idx2]

def mul(program, cur):
    idx1 = program[cur + 1]
    idx2 = program[cur + 2]
    idx3 = program[cur + 3]

    program[idx3] = program[idx1] * program[idx2]

def part2(intcodes):
    for noun, verb in product(range(100), range(100)):
        if run(list(intcodes), noun, verb)[0] != 19690720: continue
        return (100 * noun) + verb;

def puzzle2(path='inputs/day02.txt'):
    intcodes = parse(path)

    part1 = run(list(intcodes), noun=12, verb=2)[0]
    return part1, part2(intcodes)
