import math

def parse(path):
    with open(path) as f:
        return list(map(int,f.readlines()))

def mass2fuel(mass):
    return math.floor( mass / 3 ) - 2

def totalfuel(initial_mass):
    fuel = 0;
    mass = initial_mass
    while True:
        mass = mass2fuel(mass)
        if mass <= 0: break
        fuel += mass

    return fuel

def puzzle1(path='inputs/day01.txt'):
    masses = parse(path)

    part1 = sum(map(mass2fuel, masses))
    part2 = sum(map(totalfuel, masses))

    return part1, part2
