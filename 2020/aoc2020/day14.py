import re
import math
from itertools import zip_longest, product


def mask_value(mask, value):
    value = bin(value)[2:]

    result = []
    for v, m in zip_longest(reversed(value), reversed(mask)):
        if v == None: v = 0
        if   m == 'X': result.append(v)
        elif m == '0': result.append(m)
        elif m == '1': result.append(m)

    out = 0
    for i, x in enumerate(result):
        if x == '1': out += math.pow(2, i)

    return out

def part1(path):
    mem = {}
    mask = None
    with open(path) as f:
        for line in f.readlines():
            if line[0:4] == 'mask':
                mask = line[7:].strip()
                continue

            l = re.split('\[|\] = ', line.strip())
            addr = l[1]
            value = l[2]

            mem[addr] = mask_value(mask, int(value))

    return sum(mem.values())


def mask_address(mask, addr):
    addr = bin(int(addr))[2:]
    result = []

    for v, m in zip_longest(reversed(addr), reversed(mask)):
        if v == None: v = 0
        if   m == 'X': result.append('X')
        elif m == '0': result.append(v)
        elif m == '1': result.append('1')

    nx = len([x for x in result if x == 'X'])
    addrs = []
    for perm in product([0,1], repeat=nx):
        out = 0
        j   = 0
        for i, x in enumerate(result):
            if x == '1': out += math.pow(2, i)
            if x == 'X':
                if perm[j] == 1: out += math.pow(2, i)
                j += 1
        addrs.append(out)

    return addrs


def part2(path):
    mem = {}
    mask = None
    with open(path) as f:
        for line in f.readlines():
            if line[0:4] == 'mask':
                mask = line[7:].strip()
                continue

            l = re.split('\[|\] = ', line.strip())
            addr = l[1]
            value = l[2]

            for a in mask_address(mask, addr):
                mem[a] = int(value)

    return sum(mem.values())


def puzzle14(path='inputs/day14.txt'):
    return part1(path), part2(path)
