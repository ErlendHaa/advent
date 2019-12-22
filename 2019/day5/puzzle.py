import logging

def parse(path):
    with open(path, mode='r') as f:
        return [int(x) for x in f.readline().split(',')]

def run(program, testid):
    ip = 0;
    output = []

    while True:
        opcode, C, B, A = instruction( program, ip )

        if   opcode == 1: ip = add(  program, ip, C, B, A)
        elif opcode == 2: ip = mul(  program, ip, C, B, A)
        elif opcode == 3: ip = put(  program, ip, testid)
        elif opcode == 4: ip = get(  program, ip, output)
        elif opcode == 5: ip = jumpt(program, ip, C, B)
        elif opcode == 6: ip = jumpf(program, ip, C, B)
        elif opcode == 7: ip = less( program, ip, C, B, A)
        elif opcode == 8: ip = equal(program, ip, C, B, A)
        elif opcode == 99:
            logging.warning('Program finished with code 99')
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

def get(program, ip, output):
    val = program[ program[ ip + 1] ]
    output.append(val)
    return ip + 2

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

if __name__ == '__main__':
    intcodes = parse('input.txt')
    part1 = run(list(intcodes), 1)[-1]
    part2 = run(list(intcodes), 5)[0]

    print('Part 1: {}'.format(part1))
    print('Part 2: {}'.format(part2))
