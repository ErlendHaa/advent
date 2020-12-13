import math
from .point import Point

def parse(path):
    with open(path) as f:
        return [(x[0], int(x[1:])) for x in f.readlines()]

def part1(actions):
    directions = [Point(0, 1), Point(-1, 0), Point(0, -1), Point(1, 0)] # East, South, West, North

    pos = Point(0, 0)
    psi = 0 # East

    for instr, value in actions:
        if   instr == 'N': pos.y += value
        elif instr == 'S': pos.y -= value
        elif instr == 'E': pos.x += value
        elif instr == 'W': pos.x -= value
        elif instr == 'F': pos += directions[psi] * value
        elif instr == 'R': psi = int((psi + value / 90) % 4)
        elif instr == 'L': psi = int((psi - value / 90) % 4)

    return abs(pos.x + pos.y)

def part2(actions):
    directions = [Point(0, 1), Point(-1, 0), Point(0, -1), Point(1, 0)] # East, South, West, North

    ship = Point(0, 0)
    wayp = Point(10, 1) # Relative to ship

    for instr, value in actions:
        if   instr == 'N': wayp.y += value
        elif instr == 'S': wayp.y -= value
        elif instr == 'E': wayp.x += value
        elif instr == 'W': wayp.x -= value
        elif instr == 'F': ship += wayp * value
        elif instr == 'R': wayp = wayp.rotate(-math.radians(value), Point(0,0))
        elif instr == 'L': wayp = wayp.rotate(math.radians(value),  Point(0,0))

    return abs(ship.x) + abs(ship.y)


def puzzle12(path='inputs/day12.txt'):
    actions = parse(path)

    return part1(actions), part2(actions)
