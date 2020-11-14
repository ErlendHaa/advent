import logging
from collections import deque

from . import helpers

def parse(path):
    with open(path, mode='r') as f:
        return [int(x) for x in f.readline().split(',')]


def puzzle9(path='inputs/day09.txt'):
    tape = parse(path)
    comp1 = helpers.computer('Computer 1', tape, [1])()
    comp2 = helpers.computer('Computer 1', tape, [2])()

    return comp1.out[0], comp2.out[0]
