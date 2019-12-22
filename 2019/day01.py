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

if __name__ == '__main__':
    masses = parse('inputs/day01.txt')

    print('Part 1: {}'.format(sum(map(mass2fuel, masses))))
    print('Part 2: {}'.format(sum(map(totalfuel, masses))))
