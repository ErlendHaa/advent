from itertools import product

def parse(path):
    with open(path, mode='r') as f:
        return [int(x) for x in f.readline().split(',')]

def run(program):
    ip = 0;

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

def restore(program, noun, verb):
    instance = list(program)
    instance[1] = noun
    instance[2] = verb
    return instance

def part2(intcodes, combinations):
    for x, y in combinations:
        program = restore(intcodes, x, y)
        if run(program)[0] != 19690720: continue
        return (100 * x) + y;

if __name__ == '__main__':
    intcodes = parse('input.txt')

    program = restore(intcodes, 12, 2)
    part1   = run(program)

    combi = itertools.product(range(100), range(100))
    part2 = part2(intcodes, combi)

    print('Part 1: {}'.format(part1[0]))
    print('Part 2: {}'.format(part2))
