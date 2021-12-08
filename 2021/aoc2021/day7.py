from collections import defaultdict


def parse(inputfile):
    return list(map(int, open(inputfile).read().split(',')))

def diff(x, y):
    return abs(x - y)

def sumofnaturalnumbers(x, y):
    n = diff(x, y)
    return int((n * (n + 1)) / 2)

def findposition(crabs, costfunc):
    costs = defaultdict(lambda: 0)

    for pos in range(min(crabs), max(crabs)):
        for crab in crabs:
            costs[pos] += costfunc(pos, crab)

    return min([x for x in costs.values()])

def day7_part1(inputfile):
    crabs = parse(inputfile)
    return findposition(crabs, diff)

def day7_part2(inputfile):
    crabs = parse(inputfile)
    singlestatment(inputfile)
    return findposition(crabs, sumofnaturalnumbers)

def singlestatment(inputfile):
    """
    People keep saying stuff like "It ain't stupid if it works". Well, I disagree...
    """
    print('part 1: {}\npart 2: {}'.format(*[(lambda ps, fn: min([sum([fn(abs(p - x)) for x in ps]) for p in range(min(ps), max(ps))]))(list(map(int, open(inputfile).read().split(','))), fn) for fn in [lambda x: x, lambda x: (x*(x + 1))//2]]))
