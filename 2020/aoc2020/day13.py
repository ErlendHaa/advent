import math

def parse(path):
    with open(path) as f:
        time = int(f.readline())
        bus = f.readline().strip().split(',')

        return time, bus

    return step * i

def part2(busses):
    busses = [(offset, int(x)) for offset, x in enumerate(busses) if x != 'x']

    step = 1
    time = 0
    for i, (delay, bus) in enumerate(busses[1:]):
        step *= busses[i][1]
        while (time + delay) % bus != 0:
            time += step

    return time


def puzzle13(path='inputs/day13.txt'):
    time, busses = parse(path)

    inservice = [int(bus) for bus in busses if bus != 'x']
    wait = [math.ceil(time/x) * x - time for x in inservice]
    part1 = inservice[wait.index(min(wait))]  * min(wait)

    return part1, part2(busses)
