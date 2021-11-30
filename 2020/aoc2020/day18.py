import numpy as np
def prep(elements):
    tmp = []
    for elem in elements:
        if   elem == ' ': tmp.append(',')
        elif elem == '+': tmp.append("'+'")
        elif elem == '*': tmp.append("'*'")
        else: tmp.append(elem)

    return ''.join(tmp)

def parse(path):
    with open(path) as f:
        return [eval(prep(line.strip())) for line in f.readlines()]

def solve(equation):
    result  = 0
    operand = '+'
    for elem in equation:
        if elem == '+' or elem == '*':
            operand = elem
            continue

        if isinstance(elem, tuple): value = solve(elem)
        else:                       value = int(elem)

        if operand == '+': result += value
        if operand == '*': result *= value

    return result

def solvev2(equation):
    step1 = [0]
    operand = '+'
    for elem in equation:
        if elem == '+' or elem == '*':
            operand = elem
            continue

        if isinstance(elem, tuple): value = solvev2(elem)
        else:                       value = int(elem)

        if operand == '+': step1[-1] += value
        if operand == '*': step1.append(value)

    return np.prod(step1)

def puzzle18(path='inputs/day18.txt'):
    equations = parse(path)
    part1 = sum([solve(x) for x in equations])
    part2 = sum([solvev2(x) for x in equations])
    return part1, part2
