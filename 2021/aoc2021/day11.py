import numpy as np

def parse(inputfile):
    return np.array([
        [int(x) for x in line.strip('\n')]
        for line
        in open(inputfile).readlines()
    ])

def adjecent(x, y, shape):
    xlim, ylim = shape
    for xs in range(x - 1, x + 2):
        if xs < 0:     continue
        if xs >= xlim: continue
        for ys in range(y - 1, y + 2):
            if ys < 0:              continue
            if ys >= ylim:          continue
            if xs == x and ys == y: continue
            yield xs, ys

def gensquids(shape):
    xlim, ylim = shape
    for x in range(xlim):
        for y in range(ylim):
            yield x, y

def increase(squids):
    squids += 1

def flash(squids):
    flashed = set([])

    while True:
        prev = len(flashed)

        for x, y in gensquids(squids.shape):
            if squids[x, y] <= 9: continue
            if (x, y) in flashed: continue

            flashed.add((x,y))
            for other in adjecent(x, y, squids.shape):
                squids[other] += 1

        if len(flashed) == prev: break

    return flashed

def reset(squids, flashed):
    for squid in flashed:
        squids[squid] = 0
    return squids


def simulate(squids, days):
    flashes = 0
    for i in range(days):
        increase(squids)
        flashed = flash(squids)
        reset(squids, flashed)
        flashes += len(flashed)

    return flashes

def findsync(squids):
    day = 0
    while np.sum(squids) > 0:
        increase(squids)
        flashed = flash(squids)
        reset(squids, flashed)
        day += 1

    return day

def day11_part1(inputfile):
    squids = parse(inputfile)
    return simulate(squids, 100)

def day11_part2(inputfile):
    squids = parse(inputfile)
    return findsync(squids)

