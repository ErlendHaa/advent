import logging
from collections import deque

from intcode import computer

def parse(path):
    with open(path, mode='r') as f:
        return [int(x) for x in f.readline().split(',')]
if __name__ == '__main__':
    tape = parse('inputs/day09.txt')
    comp1 = computer('Computer 1', tape, [1])()
    comp2 = computer('Computer 1', tape, [2])()

    print('Part 1: {}'.format(comp1.out[0]))
    print('Part 2: {}'.format(comp2.out[0]))
